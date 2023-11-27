
INSERT INTO stocks_available (stock_id, symbol, quantity) VALUES 
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c1', 'AAPL', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c2', 'AMZN', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c3', 'TSLA', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c4', 'MSFT', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c5', 'NFLX', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c6', 'GOOGL', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c7', 'NVDA', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c8', 'META', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c9', 'WMT', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c10', 'SHEL', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c11', 'LTMAY', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c12', 'COMP', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c13', 'MA', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c14', 'PG', 2.0),
('a1a7f2ca-a5ee-4413-b321-822eadb5b5c15', 'AVGO', 2.0)

ON CONFLICT (symbol) DO NOTHING;

