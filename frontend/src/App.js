import React from 'react';
import QueryComponent from './QueryComponent'; // Ensure this path is correct
import './App.css'; // Import updated CSS for background and styling

function App() {
    return (
        <div className="App">
            <div className="app-wrapper"> {/* Wrapper for background */}
                <h1 className="app-heading">Welcome to the Query Interface</h1>
                <QueryComponent />
            </div>
        </div>
    );
}

export default App;
