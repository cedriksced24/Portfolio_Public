import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';

function AddTransaction({ addTransaction }) {
  // State to store transaction amount
  const [amount, setAmount] = useState('');
  // State to store transaction type (income or expense)
  const [type, setType] = useState('income');
  // State to store transaction description
  const [description, setDescription] = useState('');

  // Get the current date in DD.MM format
  const getCurrentDate = () => {
    const date = new Date();
    return `${date.getDate().toString().padStart(2, '0')}.${(date.getMonth() + 1).toString().padStart(2, '0')}`;
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!description || !amount) return;

    // Create a new transaction object
    const newTransaction = {
      id: uuidv4(), // Unique ID for the transaction
      amount: parseFloat(amount), // Convert amount to a number
      type, // Transaction type (income or expense)
      description, // Transaction description
      date: getCurrentDate(), // Current date in DD.MM format
    };

    // Pass the new transaction to the parent component
    addTransaction(newTransaction);

    // Reset form fields
    setAmount('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Input for transaction description */}
      <input
        type="text"
        placeholder="Beschreibung"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      {/* Input for transaction amount */}
      <input
        type="number"
        placeholder="Betrag"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />

      {/* Dropdown to select transaction type */}
      <select value={type} onChange={(e) => setType(e.target.value)}>
        <option value="income">Einnahme</option>
        <option value="expense">Ausgabe</option>
      </select>

      {/* Button to submit the transaction */}
      <button type="submit">Hinzufügen</button>
    </form>
  );
}

export default AddTransaction;
