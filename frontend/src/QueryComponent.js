import React, { useState } from 'react';
import './QueryComponent.css'; // Import CSS for styling

const QueryComponent = () => {
    const [query, setQuery] = useState('');
    const [responses, setResponses] = useState([]);
    const [formattedResponse, setFormattedResponse] = useState(null); // Store the formatted response
    const [showFormattedResponse, setShowFormattedResponse] = useState(false); // Control when to show the formatted response

    const submitQuery = async () => {
        if (!query.trim()) return; // Prevent empty submissions

        try {
            const res = await fetch('http://127.0.0.1:8000/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: query }),
            });

            if (!res.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await res.json();
            setResponses(prev => [...prev, { query, response: data.response }]);
            setFormattedResponse(data.formatted_response); // Store the formatted response
            setShowFormattedResponse(false); // Reset display state for the formatted response
            setQuery(''); // Clear the input after submission
        } catch (error) {
            console.error('Error:', error);
            setResponses(prev => [...prev, { query, response: 'An error occurred while fetching the response.' }]);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-box">
                {responses.map((item, index) => (
                    <div key={index} className="chat-message">
                        <div className="user-query">You: {item.query}</div>
                        <div className="bot-response">Bot: {item.response}</div>
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your query"
                onKeyPress={(e) => e.key === 'Enter' && submitQuery()} // Submit on Enter key
            />
            <button onClick={submitQuery}>Submit</button>

            {formattedResponse && ( // Only show the button if we have a formatted response
                <button 
                    className="context-button"
                    onClick={() => setShowFormattedResponse(!showFormattedResponse)}
                >
                    Retrieved Context
                </button>
            )}

            {showFormattedResponse && ( // Show formatted response when the button is clicked
                <div className="formatted-response">
                    <h3>Retrieved Context:</h3>
                    <p>{formattedResponse}</p>
                </div>
            )}
        </div>
    );
};

export default QueryComponent;
