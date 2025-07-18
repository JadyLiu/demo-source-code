import unittest
from risk_manager import RiskManager

class TestRiskManager(unittest.TestCase):
    def setUp(self):
        self.risk_manager = RiskManager(max_position_size=0.1, max_portfolio_risk=0.02)

    def test_calculate_position_size(self):
        portfolio_value = 100000
        entry_price = 100
        stop_loss = 95
        position_size = self.risk_manager.calculate_position_size(
            portfolio_value, entry_price, stop_loss
        )
        self.assertEqual(position_size, 100)

    def test_calculate_var(self):
        returns = [-0.01, -0.02, 0.01, 0.02, 0.03]
        var = self.risk_manager.calculate_var(returns, confidence_level=0.05)
        self.assertAlmostEqual(var, -0.02)

    def test_calculate_sharpe_ratio(self):
        returns = [0.01, 0.02, -0.01, 0.03, 0.02]
        sharpe_ratio = self.risk_manager.calculate_sharpe_ratio(returns, risk_free_rate=0.02)
        self.assertGreater(sharpe_ratio, 0)

    def test_calculate_max_drawdown(self):
        portfolio_values = [100000, 105000, 110000, 108000, 105000, 115000]
        max_drawdown = self.risk_manager.calculate_max_drawdown(portfolio_values)
        self.assertAlmostEqual(max_drawdown, 0.045454545454545456)

    def test_check_position_limits(self):
        portfolio_value = 100000
        positions = {"AAPL": 1000, "GOOGL": 500}
        prices = {"AAPL": 100, "GOOGL": 2000}
        violations = self.risk_manager.check_position_limits(
            portfolio_value, positions, prices
        )
        self.assertTrue(violations["AAPL"])
        self.assertTrue(violations["GOOGL"])

    def test_suggest_rebalancing(self):
        portfolio_value = 100000
        positions = {"AAPL": 1000, "GOOGL": 500}
        prices = {"AAPL": 100, "GOOGL": 2000}
        suggestions = self.risk_manager.suggest_rebalancing(
            portfolio_value, positions, prices
        )
        self.assertEqual(suggestions["AAPL"], -900)
        self.assertLess(suggestions["GOOGL"], 0)

if __name__ == "__main__":
    unittest.main()