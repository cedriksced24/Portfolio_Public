import React from 'react';

function ExpenseList({ transactions, deleteTransaction }) {
  return (
    <div>
      <h2>Ausgaben</h2>
      <ul className="list">
        {transactions.filter(t => t.type === 'expense').map((t) => (
          <li key={t.id} className="list-item">
            {t.description} ({t.date}): {t.amount} €
            <button onClick={() => deleteTransaction(t.id)} className="delete-button">Löschen</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ExpenseList;
