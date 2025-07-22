import unittest
from risk_manager import RiskManager


class TestRiskManager(unittest.TestCase):
    def setUp(self):
        self.risk_manager = RiskManager()

    def test_calculate_position_size(self):
        # Test normal case
        result = self.risk_manager.calculate_position_size(
            portfolio_value=100000, entry_price=100, stop_loss=90
        )
        self.assertEqual(result, 100)  # min(2000 shares by risk, 1000 shares by size)

        # Test when stop loss equals entry price (no risk)
        result = self.risk_manager.calculate_position_size(
            portfolio_value=100000, entry_price=100, stop_loss=100
        )
        self.assertEqual(result, 0)

        # Test when risk limit is more restrictive
        result = self.risk_manager.calculate_position_size(
            portfolio_value=100000, entry_price=100, stop_loss=50
        )
        self.assertEqual(result, 40)  # min(40 shares by risk, 1000 shares by size)

    def test_calculate_var(self):
        returns = [0.01, -0.02, 0.03, -0.04, 0.05, -0.06, 0.07, -0.08, 0.09, -0.10]
        var = self.risk_manager.calculate_var(returns, confidence_level=0.05)
        self.assertAlmostEqual(var, -0.10, places=2)

        # Test empty returns
        self.assertEqual(self.risk_manager.calculate_var([]), 0.0)

    def test_calculate_sharpe_ratio(self):
        returns = [0.01, 0.02, 0.03, 0.04, 0.05]
        sharpe = self.risk_manager.calculate_sharpe_ratio(returns)
        self.assertGreater(sharpe, 0)

        # Test with insufficient data
        self.assertEqual(self.risk_manager.calculate_sharpe_ratio([0.01]), 0.0)

    def test_calculate_max_drawdown(self):
        values = [100, 150, 120, 180, 160, 200, 110]
        max_dd = self.risk_manager.calculate_max_drawdown(values)
        self.assertAlmostEqual(max_dd, 0.45, places=2)  # (200 - 110) / 200

        # Test with insufficient data
        self.assertEqual(self.risk_manager.calculate_max_drawdown([100]), 0.0)

    def test_check_position_limits(self):
        positions = {"AAPL": 100, "GOOG": 50}
        prices = {"AAPL": 150, "GOOG": 2500}
        violations = self.risk_manager.check_position_limits(
            portfolio_value=100000, positions=positions, prices=prices
        )
        self.assertTrue(violations["AAPL"])  # 15000 / 100000 = 15% > 10%
        self.assertTrue(violations["GOOG"])  # 125000 / 100000 = 125% > 10%

    def test_suggest_rebalancing(self):
        positions = {"AAPL": 100, "GOOG": 50}
        prices = {"AAPL": 150, "GOOG": 2500}
        suggestions = self.risk_manager.suggest_rebalancing(
            portfolio_value=100000, positions=positions, prices=prices
        )
        self.assertEqual(suggestions["AAPL"], -34)  # Sell 34 shares to meet 10% limit
        self.assertEqual(suggestions["GOOG"], -46)  # Sell 46 shares to meet 10% limit


if __name__ == "__main__":
    unittest.main()