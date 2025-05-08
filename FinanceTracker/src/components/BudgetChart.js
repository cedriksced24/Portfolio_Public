import React from 'react';
import { PieChart, Pie, Cell } from 'recharts';

function BudgetChart({ income, expenses }) {
  // Prepare data for the pie chart
  const data = [
    { name: 'Einnahmen', value: income },   // Income slice
    { name: 'Ausgaben', value: expenses },   // Expenses slice
  ];

  return (
    <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
      {/* Pie chart displaying income and expenses */}
      <PieChart width={300} height={300}>
        <Pie data={data} dataKey="value" outerRadius={100} fill="#8884d8">
          {/* Cell for income (green) */}
          <Cell fill="#82ca9d" />
          {/* Cell for expenses (orange) */}
          <Cell fill="#ff8042" />
        </Pie>
      </PieChart>
    </div>
  );
}

export default BudgetChart;
