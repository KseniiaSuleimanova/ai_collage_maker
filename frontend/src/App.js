import React, { useState } from 'react';

function App() {
  const [counter, setCounter] = useState(0);

  const incrementCounter = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/increment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      setCounter(data.counter);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Counter: {counter}</h1>
      <button onClick={incrementCounter}>Increment</button>
    </div>
  );
}

export default App;
