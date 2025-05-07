import React from 'react';

function IncomeList({ transactions, deleteTransaction }) {
  return (
    <div>
      <h2>Einnahmen</h2>
      <ul className="list">
        {transactions.filter(t => t.type === 'income').map((t) => (
          <li key={t.id} className="list-item">
            {t.description} ({t.date}): {t.amount} €
            <button onClick={() => deleteTransaction(t.id)} className="delete-button">Löschen</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default IncomeList;
