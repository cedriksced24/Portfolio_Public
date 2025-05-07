import React, { useState, useEffect } from 'react';

const stockSymbols = [
  'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'AMD', 'INTC', // Tech
  'BABA', 'JD', 'PDD', 'TCEHY', 'NIO', 'XPEV', 'LI', 'BYDDY', 'BIDU', 'NTES',       // China Tech
  'KO', 'PEP', 'MCD', 'SBUX', 'YUM', 'WMT', 'COST', 'TGT', 'KR', 'CVS',             // Consumer Goods
  'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'PYPL', 'SQ',                 // Financials
  'DIS', 'CMCSA', 'WBD', 'NKE', 'UA', 'ADDYY', 'LULU', 'RCL', 'CCL', 'MAR',          // Entertainment & Leisure
  'XOM', 'CVX', 'COP', 'BP', 'SHEL', 'TOT', 'ENB', 'KMI', 'PBR', 'VLO',              // Energy
  'PFE', 'MRNA', 'JNJ', 'MRK', 'BMY', 'AMGN', 'LLY', 'ABBV', 'CVS', 'CAH',           // Healthcare
  'BA', 'LMT', 'NOC', 'GD', 'RTX', 'HON', 'MMM', 'GE', 'CAT', 'DE',                  // Industrials
  'TM', 'HMC', 'F', 'GM', 'TSLA', 'NIO', 'RIVN', 'LCID', 'FSR', 'NKLA',              // Automotive
  'ORCL', 'SAP', 'CRM', 'ADBE', 'INTU', 'CSCO', 'IBM', 'TXN', 'QCOM', 'AVGO',        // Enterprise Tech
  'PG', 'UL', 'CL', 'KMB', 'GIS', 'HSY', 'K', 'CPB', 'MO', 'PM'                      // Consumer Staples
];

function StockSuggestion() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchSymbol, setSearchSymbol] = useState('AAPL'); // Standardwert
  const [autoStock, setAutoStock] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => {
      const randomSymbol = stockSymbols[Math.floor(Math.random() * stockSymbols.length)];
      fetchAutoStock(randomSymbol);
    }, 10000); // 10 Sekunden

    return () => clearInterval(interval);
  }, []);

  const fetchStocks = async (symbol) => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(
        `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=YRCGLQL0P9C9E3H2`
      );

      if (!response.ok) {
        throw new Error('Fehler beim Abrufen der Aktieninformationen');
      }

      const data = await response.json();
      const timeSeries = data['Time Series (Daily)'];

      if (timeSeries) {
        const latestDate = Object.keys(timeSeries)[0];
        const latestData = timeSeries[latestDate];
        const stockInfo = {
          symbol: symbol.toUpperCase(),
          date: latestDate,
          price: latestData['4. close'],
        };
        return stockInfo;
      } else {
        throw new Error('Keine Daten verfügbar');
      }
    } catch (err) {
      throw new Error('Fehler: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchAutoStock = async (symbol) => {
    try {
      const stockInfo = await fetchStocks(symbol);
      setAutoStock(stockInfo);
    } catch (err) {
      setError(err.message);
    }
  };

  const fetchManualStock = async () => {
    try {
      const stockInfo = await fetchStocks(searchSymbol);
      setStocks([stockInfo]);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleInputChange = (e) => {
    setSearchSymbol(e.target.value);
  };

  return (
    <div className="stock-suggestion">
      <h2>Investitionsvorschläge</h2>
      <div className="stock-search">
        <input
          type="text"
          placeholder="Aktien-Symbol (z.B. AAPL, TSLA)"
          value={searchSymbol}
          onChange={handleInputChange}
          className="stock-input"
        />
        <button onClick={fetchManualStock} className="stock-button">
          Aktie suchen
        </button>
      </div>
      {loading && <p>Laden...</p>}
      {error && <p className="error">{error}</p>}
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
      {autoStock && (
        <div className="auto-stock">
          <h3>Automatische Aktienanzeige:</h3>
          <p>{autoStock.symbol} - Preis am {autoStock.date}: {autoStock.price} USD</p>
        </div>
      )}
    </div>
  );
}

export default StockSuggestion;
