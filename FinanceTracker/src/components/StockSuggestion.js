import React, { useState, useEffect } from 'react';

const stockSymbols = [
  // Array of popular stock symbols from various sectors
  'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'AMD', 'INTC',
  'BABA', 'JD', 'PDD', 'TCEHY', 'NIO', 'XPEV', 'LI', 'BYDDY', 'BIDU', 'NTES',
  'KO', 'PEP', 'MCD', 'SBUX', 'YUM', 'WMT', 'COST', 'TGT', 'KR', 'CVS',
  'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'PYPL', 'SQ',
  'DIS', 'CMCSA', 'WBD', 'NKE', 'UA', 'ADDYY', 'LULU', 'RCL', 'CCL', 'MAR',
  'XOM', 'CVX', 'COP', 'BP', 'SHEL', 'TOT', 'ENB', 'KMI', 'PBR', 'VLO',
  'PFE', 'MRNA', 'JNJ', 'MRK', 'BMY', 'AMGN', 'LLY', 'ABBV', 'CVS', 'CAH',
  'BA', 'LMT', 'NOC', 'GD', 'RTX', 'HON', 'MMM', 'GE', 'CAT', 'DE',
  'TM', 'HMC', 'F', 'GM', 'TSLA', 'NIO', 'RIVN', 'LCID', 'FSR', 'NKLA',
  'ORCL', 'SAP', 'CRM', 'ADBE', 'INTU', 'CSCO', 'IBM', 'TXN', 'QCOM', 'AVGO',
  'PG', 'UL', 'CL', 'KMB', 'GIS', 'HSY', 'K', 'CPB', 'MO', 'PM'
];

function StockSuggestion() {
  // State for stock data and UI feedback
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchSymbol, setSearchSymbol] = useState('AAPL');  // Default symbol
  const [autoStock, setAutoStock] = useState(null);

  // Automatically fetch a random stock every 10 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      const randomSymbol = stockSymbols[Math.floor(Math.random() * stockSymbols.length)];
      fetchAutoStock(randomSymbol);
    }, 10000);

    return () => clearInterval(interval);  // Cleanup on unmount
  }, []);

  // Fetch stock data from API
  const fetchStocks = async (symbol) => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(
        `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey="URAPIKEY"`
      );

      if (!response.ok) {
        throw new Error('Failed to fetch stock data');
      }

      const data = await response.json();
      const timeSeries = data['Time Series (Daily)'];

      if (timeSeries) {
        const latestDate = Object.keys(timeSeries)[0];
        const latestData = timeSeries[latestDate];
        // Extract relevant stock information
        const stockInfo = {
          symbol: symbol.toUpperCase(),
          date: latestDate,
          price: latestData['4. close'],
        };
        return stockInfo;
      } else {
        throw new Error('No data available');
      }
    } catch (err) {
      throw new Error('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch stock for the automatic suggestion
  const fetchAutoStock = async (symbol) => {
    try {
      const stockInfo = await fetchStocks(symbol);
      setAutoStock(stockInfo);
    } catch (err) {
      setError(err.message);
    }
  };

  // Fetch stock based on user input
  const fetchManualStock = async () => {
    try {
      const stockInfo = await fetchStocks(searchSymbol);
      setStocks([stockInfo]);
    } catch (err) {
      setError(err.message);
    }
  };

  // Handle changes in the search input field
  const handleInputChange = (e) => {
    setSearchSymbol(e.target.value);
  };

  return (
    <div className="stock-suggestion">
      <h2>Investitionsvorschläge</h2>
      <div className="stock-search">
        {/* Input field for manual stock search */}
        <input
          type="text"
          placeholder="Aktien-Symbol (z.B. AAPL, TSLA)"
          value={searchSymbol}
          onChange={handleInputChange}
          className="stock-input"
        />
        {/* Button to trigger stock search */}
        <button onClick={fetchManualStock} className="stock-button">
          Aktie suchen
        </button>
      </div>
      {/* Display loading message */}
      {loading && <p>Laden...</p>}
      {/* Display error message */}
      {error && <p className="error">{error}</p>}
      {/* Display manually searched stock */}
      {stocks.length > 0 && (
        <div className="stock-result">
          <h3>Suchergebnis:</h3>
          {stocks.map((stock, index) => (
            <p key={index}>
              {stock.symbol} - Preis am {stock.date}: {stock.price} USD
            </p>
          ))}
        </div>
      )}
      {/* Display automatically suggested stock */}
      {autoStock && (
        <div className="auto-stock">
          <h3>Automatische Aktienanzeige:</h3>
          <p>
            {autoStock.symbol} - Preis am {autoStock.date}: {autoStock.price} USD
          </p>
        </div>
      )}
    </div>
  );
}

export default StockSuggestion;
