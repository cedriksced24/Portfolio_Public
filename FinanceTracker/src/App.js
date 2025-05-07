import React, { useState, useEffect } from 'react';
import { saveToLocalStorage, getFromLocalStorage } from './utils/storage';
import ExpenseList from './components/ExpenseList';
import IncomeList from './components/IncomeList';
import AddTransaction from './components/AddTransaction';
import BudgetChart from './components/BudgetChart';
import StockSuggestion from './components/StockSuggestion';  // Import der Komponente
import './styles/style.css';

function App() {
  const [transactions, setTransactions] = useState(getFromLocalStorage('transactions'));
  const [monthFilter, setMonthFilter] = useState('');

  useEffect(() => {
    saveToLocalStorage('transactions', transactions);
  }, [transactions]);

  const addTransaction = (transaction) => {
    setTransactions([...transactions, transaction]);
  };

  const deleteTransaction = (id) => {
    setTransactions(transactions.filter((t) => t.id !== id));
  };

  const income = transactions
    .filter((t) => t.type === 'income')
    .reduce((acc, t) => acc + parseFloat(t.amount), 0);

  const expenses = transactions
    .filter((t) => t.type === 'expense')
    .reduce((acc, t) => acc + parseFloat(t.amount), 0);

  const handleMonthChange = (e) => {
    setMonthFilter(e.target.value);
  };

  const filteredTransactions = monthFilter
    ? transactions.filter((t) => t.date.endsWith(monthFilter))
    : transactions;

  return (
    <div className="container">
      <h1>Finanz-Dashboard</h1>
      <AddTransaction addTransaction={addTransaction} />

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

      <BudgetChart income={income} expenses={expenses} />
      <IncomeList transactions={filteredTransactions} deleteTransaction={deleteTransaction} />
      <ExpenseList transactions={filteredTransactions} deleteTransaction={deleteTransaction} />

      {/* Einbau der StockSuggestion Komponente */}
      <StockSuggestion />
    </div>
  );
}

export default App;
