import unittest
import pandas as pd
from datetime import datetime, timedelta
from data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()

    def test_generate_sample_data(self):
        symbol = "AAPL"
        data = self.loader.generate_sample_data(symbol)
        self.assertEqual(len(data), 252)
        self.assertListEqual(list(data.columns), ["open", "high", "low", "close", "volume"])

    def test_load_csv_data(self):
        symbol = "AAPL"
        file_path = "test_data.csv"
        # Create a test CSV file
        test_data = pd.DataFrame({
            "open": [100, 101],
            "high": [102, 103],
            "low": [99, 100],
            "close": [101, 102],
            "volume": [100000, 101000],
        })
        test_data.index = pd.date_range(start=datetime.now() - timedelta(days=1), periods=2)
        test_data.to_csv(file_path)

        data = self.loader.load_csv_data(file_path, symbol)
        self.assertEqual(len(data), 2)
        self.assertListEqual(list(data.columns), ["open", "high", "low", "close", "volume"])

    def test_get_price_data(self):
        symbol = "AAPL"
        self.loader.generate_sample_data(symbol)
        data = self.loader.get_price_data(symbol)
        self.assertEqual(len(data), 252)

    def test_get_latest_price(self):
        symbol = "AAPL"
        self.loader.generate_sample_data(symbol)
        latest_price = self.loader.get_latest_price(symbol)
        self.assertIsInstance(latest_price, float)

    def test_get_price_history(self):
        symbol = "AAPL"
        self.loader.generate_sample_data(symbol)
        history = self.loader.get_price_history(symbol, days=10)
        self.assertEqual(len(history), 10)

    def test_add_technical_indicators(self):
        symbol = "AAPL"
        data = self.loader.generate_sample_data(symbol)
        data_with_indicators = self.loader.add_technical_indicators(data)
        expected_columns = [
            "open", "high", "low", "close", "volume",
            "sma_10", "sma_20", "sma_50",
            "ema_12", "ema_26",
            "macd", "macd_signal", "macd_histogram",
            "bb_middle", "bb_upper", "bb_lower",
            "rsi"
        ]
        self.assertListEqual(list(data_with_indicators.columns), expected_columns)

    def test_get_multiple_symbols(self):
        symbols = ["AAPL", "GOOGL"]
        data = self.loader.get_multiple_symbols(symbols)
        self.assertEqual(len(data), 2)
        self.assertIn("AAPL", data)
        self.assertIn("GOOGL", data)

if __name__ == "__main__":
    unittest.main()