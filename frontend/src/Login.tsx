import { useState } from "react";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");


async function loginAction(username: string, password: string) {

  const response = await fetch("http://localhost:8000/login", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.access_token); // Store token
      // alert("Login successful!");
  } else {
      alert("Invalid credentials");
  }

  window.location.href = "/";
}

const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token); // Store token
        alert("Login successful!");
    } else {
        alert("Invalid credentials");
    }
};

  return (
    <div className="flex flex-col w-full h-screen gap-4 justify-center items-center">
      <h2>Login</h2>
      <form className="flex flex-col items-center gap-3" onSubmit={handleLogin}>
        <input className="p-2" type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        <input className="p-2" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button className="w-60">Login</button>
      </form>
      <button className="w-60" onClick={() => {loginAction('tony', '123')}}>Login as CEO</button>
      <button className="w-60" onClick={() => {loginAction('sam', '456')}}>Login as Manager</button>
      <button className="w-60" onClick={() => {loginAction('rob', '789')}}>Login as Employee</button>
    </div>
  );
};

export default Login;
