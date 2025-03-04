from pydantic import BaseModel
from typing import List
from ollama import chat, embed, ChatResponse
from qdrant_client import QdrantClient
import sqlite3

class TextRequest(BaseModel):
    text: str

class Message(BaseModel):
    role: str
    content: str
    
class RequestModel(BaseModel):
    messages: List[Message]

print("Entered Utils")
client = QdrantClient(url='http://localhost:6333')
conn = sqlite3.connect('./data/erp_database.db')
cursor = conn.cursor()


def get_average_salary():
    """
    Asynchronously retrieves the average salary from the 'erp_table'.

    Returns:
        float: The average salary.

    Raises:
        Exception: If there is an issue with the database query.
    """
    cursor.execute("SELECT AVG(Salary) FROM erp_table")
    average_salary = cursor.fetchone()[0]
    return average_salary

def get_person_information(name: str):
    """
    Asynchronously retrieves information about a person from the database based on their name.

    Args:
        name (str): The name of the person whose information is to be retrieved.

    Returns:
        str: A formatted string containing the person's information if found, 
                otherwise a message indicating no information was found for the given name.

    Raises:
        Exception: If there is an issue with the database query or connection.
    """
    cursor.execute("SELECT * FROM erp_table WHERE [Employee Name] = ?", (name,))
    person_info = cursor.fetchone()
    if person_info: 
        f"""
            Reply from get person Information {name}
            "Employee ID": {person_info[0]},
            "Employee Name": {person_info[1]},
            "Department": {person_info[2]},
            "Role": {person_info[3]},
            "Salary": {person_info[4]}
        """
    else:
        return f"No information found for the given name {name}"



class OllamaUser:
    global_username = ''
    def __init__(self, username: str, position: str):
        self.username = username
        self.position = position
        all_tools = {
            'ceo': [get_average_salary, get_person_information],
            'manager': [get_person_information],
            'employee': [],
        }
        self.tools = all_tools[position]
        self.available_functions = {
            'get_average_salary' : get_average_salary,
            'get_person_information': get_person_information,
            'get_my_information' : self.get_my_information
        }
        
    
    async def get_ollama_response(self, messages :List[Message], model="qwen2.5", embed_model='granite-embedding:278m'):
        try: 
            # messages.append({'role': 'user', 'content': 'I want to query the embedding model to get relevent text in return from teh embeddding model. Give me a set of one or two questions based on teh previous chat which i can send to the embedding models to get the output return. be concise in answer and give only one or two questions.'})
            # response: ChatResponse = chat(
            #     model=model,
            #     messages=messages
            # )
            # messages.pop()
            # embedding_input = response.message.content
            # print("Embeding Input response: ", embedding_input)

            embedding_input = messages[-1]['content']
            
            response = embed(
                model=embed_model,
                input=embedding_input
            )
            vector = response["embeddings"][0]
            print('Embeddings: ', vector[:10])
            
            context = ''
            print("Tools Accissble to user: ", self.tools)
            #Getting SQL data
            response = chat(
                model=model,
                messages=[{'role': 'user', 'content': embedding_input}],
                tools=self.tools
            )

            print("Tool Response: ", response)


            for tool in response.message.tool_calls or []:
                print("Tool being called: ", tool.function.name)
                function_to_call = self.available_functions.get(tool.function.name)
                if function_to_call:
                    context += f"This is the response from {tool.function.name} having arguments {tool.function.arguments}" + str(function_to_call(**tool.function.arguments))
                else:
                    print('Function not found:', tool.function.name)

            search_result = client.query_points(
                collection_name=self.position , #query collection based on the position
                query=vector,
                with_payload=True,
                limit=2
            ).points

            context += '\n'.join([f"Context {index + 1}:\n{result.payload['text']}\n" for index, result in enumerate(search_result)])
            # print(f"Messages sent to model {messages[-1]}")
            messages[-1]["content"] += f"""Above is the user message. Be concise in answering the user message unless user tells otherwise. Below you have been provided a context retrived from the embedding model based on the user input. The context may or may not be required to answer user message. For user message like "Hello" you can reply as "hello". You can use this contextto answer if required or just reply to user message if context is not relavent. Context = {context} """
            print(f"Messages sent to model {messages[-1]}")

            response: ChatResponse = chat(
                model=model,
                messages=messages,
            )

            messages[-1]["content"] = embedding_input

            return response.message.content
        
        except Exception as e:
            print(f"An error occurred in get_ollama_response: {e}")
            return "Error in get_olama_chat"
    
    async def get_my_information(self):
        """
        Asynchronously retrieves the personal information of the user.

        Returns:
            dict: A dictionary containing the personal information of the user.
        """
        return  self.get_person_information(name=self.username)