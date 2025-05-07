import React from 'react';
import ReactDOM from 'react-dom/client';  // Neue Importweise in React 18
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
