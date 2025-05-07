import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';

function AddTransaction({ addTransaction }) {
  const [amount, setAmount] = useState('');
  const [type, setType] = useState('income');
  const [description, setDescription] = useState('');

  const getCurrentDate = () => {
    const date = new Date();
    return `${date.getDate().toString().padStart(2, '0')}.${(date.getMonth() + 1).toString().padStart(2, '0')}`;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!description || !amount) return;
    const newTransaction = {
      id: uuidv4(),
      amount: parseFloat(amount),
      type,
      description,
      date: getCurrentDate(),
    };
    addTransaction(newTransaction);
    setAmount('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Beschreibung"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <input
        type="number"
        placeholder="Betrag"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <select value={type} onChange={(e) => setType(e.target.value)}>
        <option value="income">Einnahme</option>
        <option value="expense">Ausgabe</option>
      </select>
      <button type="submit">Hinzufügen</button>
    </form>
  );
}

export default AddTransaction;
