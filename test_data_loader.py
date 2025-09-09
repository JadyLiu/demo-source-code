import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.data_loader = DataLoader()
        self.test_symbol = "TEST"
        self.test_days = 100
        
    def test_generate_sample_data(self):
        """Test that sample data generation works correctly."""
        data = self.data_loader.generate_sample_data(self.test_symbol, self.test_days)
        
        # Check data structure
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), self.test_days)
        self.assertListEqual(list(data.columns), ['open', 'high', 'low', 'close', 'volume'])
        
        # Check that high >= low, high >= close, etc.
        self.assertTrue((data['high'] >= data['close']).all())
        self.assertTrue((data['low'] <= data['close']).all())
        
    def test_get_price_data(self):
        """Test getting price data with and without date filtering."""
        # Generate test data
        self.data_loader.generate_sample_data(self.test_symbol, self.test_days)
        
        # Get full data
        full_data = self.data_loader.get_price_data(self.test_symbol)
        self.assertEqual(len(full_data), self.test_days)
        
        # Get filtered data
        start_date = (datetime.now() - timedelta(days=50)).strftime('%Y-%m-%d')
        filtered_data = self.data_loader.get_price_data(self.test_symbol, start_date=start_date)
        self.assertLess(len(filtered_data), self.test_days)
        
    def test_technical_indicators(self):
        """Test that technical indicators are calculated correctly."""
        data = self.data_loader.generate_sample_data(self.test_symbol, self.test_days)
        data_with_indicators = self.data_loader.add_technical_indicators(data)
        
        # Check that indicators are added
        expected_indicators = ['sma_10', 'sma_20', 'sma_50', 'ema_12', 'ema_26', 
                             'macd', 'macd_signal', 'macd_histogram', 
                             'bb_middle', 'bb_upper', 'bb_lower', 'rsi']
        
        for indicator in expected_indicators:
            self.assertIn(indicator, data_with_indicators.columns)
        
        # Check that RSI is between 0 and 100 (ignoring NaN values)
        self.assertTrue((data_with_indicators['rsi'].dropna() >= 0).all())
        self.assertTrue((data_with_indicators['rsi'].dropna() <= 100).all())
        
    def test_max_drawdown(self):
        """Test maximum drawdown calculation."""
        # Create test data with a known drawdown pattern
        dates = pd.date_range(end=datetime.now(), periods=10)
        prices = [100, 110, 90, 95, 80, 85, 70, 75, 60, 65]  # Max drawdown: (110-60)/110 ≈ 45.45%
        
        test_data = pd.DataFrame({
            'open': prices,
            'high': prices,
            'low': prices,
            'close': prices,
            'volume': 1000
        }, index=dates)
        
        self.data_loader.data_cache[self.test_symbol] = test_data
        
        # Calculate max drawdown
        max_dd = self.data_loader.calculate_max_drawdown(self.test_symbol)
        
        # Check result (allowing for floating point precision)
        self.assertAlmostEqual(max_dd, 45.45, places=1)
        
    def test_multiple_symbols(self):
        """Test getting data for multiple symbols."""
        symbols = ["AAPL", "GOOG", "MSFT"]
        result = self.data_loader.get_multiple_symbols(symbols, days=50)
        
        # Check that we get data for all symbols
        self.assertEqual(len(result), len(symbols))
        for symbol in symbols:
            self.assertIn(symbol, result)
            self.assertIsInstance(result[symbol], pd.DataFrame)
            self.assertEqual(len(result[symbol]), 50)


if __name__ == '__main__':
    unittest.main()