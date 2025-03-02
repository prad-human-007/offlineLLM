import { useState } from 'react'

import { ChatInterface } from './components/ChatInterface'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='w-full h-screen p-5'>
      
      <ChatInterface />
    </div>
  )
}

export default App
