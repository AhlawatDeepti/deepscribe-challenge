import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! Ask me any questions about the patient's transcript.", sender: 'ai' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // API call to the Flask backend
      const response = await axios.post('https://deepscribe-challenge-backend.onrender.com', {
        question: input
      });

      const aiMessage = { text: response.data.answer, sender: 'ai' };
      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error('Error fetching response:', error);
      const errorMessage = { text: 'Sorry, I ran into an error. Please try again.', sender: 'ai' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // --- Component Styles ---
  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      width: '100%',
      maxWidth: '768px',
      margin: '0 auto',
      boxShadow: '0 0 10px rgba(0,0,0,0.1)',
      backgroundColor: '#fff',
    },
    header: {
      padding: '16px',
      backgroundColor: '#007bff',
      color: 'white',
      textAlign: 'center',
      fontSize: '1.2rem',
      fontWeight: 'bold',
    },
    messageContainer: {
      flex: 1,
      padding: '16px',
      overflowY: 'auto',
      display: 'flex',
      flexDirection: 'column',
      gap: '12px',
    },
    message: {
      padding: '10px 14px',
      borderRadius: '18px',
      maxWidth: '75%',
      wordWrap: 'break-word',
    },
    userMessage: {
      alignSelf: 'flex-end',
      backgroundColor: '#007bff',
      color: 'white',
    },
    aiMessage: {
      alignSelf: 'flex-start',
      backgroundColor: '#e9ecef',
      color: '#343a40',
    },
    form: {
      display: 'flex',
      padding: '16px',
      borderTop: '1px solid #ddd',
    },
    input: {
      flex: 1,
      padding: '10px',
      borderRadius: '20px',
      border: '1px solid #ccc',
      marginRight: '10px',
      fontSize: '1rem',
    },
    button: {
      padding: '10px 20px',
      borderRadius: '20px',
      border: 'none',
      backgroundColor: '#007bff',
      color: 'white',
      cursor: 'pointer',
      fontSize: '1rem',
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>DeepScribe Transcript Assistant</div>
      <div style={styles.messageContainer}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              ...(msg.sender === 'user' ? styles.userMessage : styles.aiMessage)
            }}
          >
            {msg.text}
          </div>
        ))}
        {isLoading && <div style={styles.aiMessage}>Thinking...</div>}
      </div>
      <form onSubmit={handleSend} style={styles.form}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={styles.input}
          placeholder="Ask a question..."
          disabled={isLoading}
        />
        <button type="submit" style={styles.button} disabled={isLoading}>Send</button>
      </form>
    </div>
  );
};

export default App;