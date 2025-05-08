import React from 'react';

function IncomeList({ transactions, deleteTransaction }) {
  return (
    <div>
      <h2>Einnahmen</h2>
      <ul className="list">
        {/* Filter and display only transactions of type 'income' */}
        {transactions.filter(t => t.type === 'income').map((t) => (
          <li key={t.id} className="list-item">
            {/* Show description, date, and amount */}
            {t.description} ({t.date}): {t.amount} €

            {/* Button to delete this transaction */}
            <button onClick={() => deleteTransaction(t.id)} className="delete-button">
              Löschen
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default IncomeList;
