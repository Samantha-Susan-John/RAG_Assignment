import React from 'react';
import QueryComponent from './QueryComponent';
import './App.css'; 

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
