import React from 'react';
import { PieChart, Pie, Cell } from 'recharts';

function BudgetChart({ income, expenses }) {
  const data = [
    { name: 'Einnahmen', value: income },
    { name: 'Ausgaben', value: expenses },
  ];

  return (
    <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
      <PieChart width={300} height={300}>
        <Pie data={data} dataKey="value" outerRadius={100} fill="#8884d8">
          <Cell fill="#82ca9d" />
          <Cell fill="#ff8042" />
        </Pie>
      </PieChart>
    </div>
  );
}

export default BudgetChart;
