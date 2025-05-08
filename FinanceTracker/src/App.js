import React, { useState, useEffect } from 'react';
import { saveToLocalStorage, getFromLocalStorage } from './utils/storage';
import ExpenseList from './components/ExpenseList';
import IncomeList from './components/IncomeList';
import AddTransaction from './components/AddTransaction';
import BudgetChart from './components/BudgetChart';
import StockSuggestion from './components/StockSuggestion';  // Stock suggestion component
import './styles/style.css';

function App() {
  // Load transactions from localStorage or initialize as empty
  const [transactions, setTransactions] = useState(getFromLocalStorage('transactions'));

  // Current selected month filter
  const [monthFilter, setMonthFilter] = useState('');

  // Save transactions to localStorage whenever they change
  useEffect(() => {
    saveToLocalStorage('transactions', transactions);
  }, [transactions]);

  // Add a new transaction to the list
  const addTransaction = (transaction) => {
    setTransactions([...transactions, transaction]);
  };

  // Remove a transaction by ID
  const deleteTransaction = (id) => {
    setTransactions(transactions.filter((t) => t.id !== id));
  };

  // Calculate total income
  const income = transactions
    .filter((t) => t.type === 'income')
    .reduce((acc, t) => acc + parseFloat(t.amount), 0);

  // Calculate total expenses
  const expenses = transactions
    .filter((t) => t.type === 'expense')
    .reduce((acc, t) => acc + parseFloat(t.amount), 0);

  // Handle dropdown change for month filtering
  const handleMonthChange = (e) => {
    setMonthFilter(e.target.value);
  };

  // Filter transactions by selected month, if any
  const filteredTransactions = monthFilter
    ? transactions.filter((t) => t.date.endsWith(monthFilter))
    : transactions;

  return (
    <div className="container">
      <h1>Finanz-Dashboard</h1>

      {/* Add new transaction form */}
      <AddTransaction addTransaction={addTransaction} />

      {/* Month filter dropdown */}
      <div className="filter">
        <label>Monat filtern: </label>
        <select value={monthFilter} onChange={handleMonthChange}>
          <option value="">Alle</option>
          <option value=".01">Januar</option>
          <option value=".02">Februar</option>
          <option value=".03">März</option>
          <option value=".04">April</option>
          <option value=".05">Mai</option>
          <option value=".06">Juni</option>
          <option value=".07">Juli</option>
          <option value=".08">August</option>
          <option value=".09">September</option>
          <option value=".10">Oktober</option>
          <option value=".11">November</option>
          <option value=".12">Dezember</option>
        </select>
      </div>

      {/* Chart visualization of income and expenses */}
      <BudgetChart income={income} expenses={expenses} />

      {/* Display filtered income and expenses lists */}
      <IncomeList transactions={filteredTransactions} deleteTransaction={deleteTransaction} />
      <ExpenseList transactions={filteredTransactions} deleteTransaction={deleteTransaction} />

      {/* Show random stock suggestions every 10 seconds */}
      <StockSuggestion />
    </div>
  );
}

export default App;
