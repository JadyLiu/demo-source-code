import unittest

class RiskManager:
    """Risk management utilities for portfolio and position sizing."""

    def __init__(
        self, max_position_size: float = 0.1, max_portfolio_risk: float = 0.02
    ) -> None:
        self.max_position_size = max_position_size  # Max 10% of portfolio per position
        self.max_portfolio_risk = max_portfolio_risk  # Max 2% portfolio risk per trade

    def calculate_position_size(
        self, portfolio_value: float, entry_price: float, stop_loss: float
    ) -> int:
        """Calculate position size based on risk management rules."""
        # Risk per share
        risk_per_share = abs(entry_price - stop_loss)
        if risk_per_share == 0:
            return 0

        # Maximum position based on portfolio risk
        max_risk_amount = portfolio_value * self.max_portfolio_risk
        max_shares_by_risk = int(max_risk_amount / risk_per_share)

        # Maximum position based on position size limit
        max_shares_by_position_size = int((portfolio_value * self.max_position_size) / entry_price)

        # Return the minimum of the two to adhere to both constraints
        return min(max_shares_by_risk, max_shares_by_position_size)

class TestRiskManager(unittest.TestCase):
    def setUp(self):
        self.risk_manager = RiskManager()

    def test_calculate_position_size(self):
        # Test with normal values
        self.assertEqual(self.risk_manager.calculate_position_size(10000, 100, 95), 10)

        # Test with zero risk per share
        self.assertEqual(self.risk_manager.calculate_position_size(10000, 100, 100), 0)

        # Test with a very small portfolio
        self.assertEqual(self.risk_manager.calculate_position_size(100, 100, 95), 0)

        # Test with a large portfolio
        self.assertEqual(self.risk_manager.calculate_position_size(1000000, 100, 95), 1000)

        # Test with a different max position size and max portfolio risk
        custom_risk_manager = RiskManager(max_position_size=0.2, max_portfolio_risk=0.05)
        self.assertEqual(custom_risk_manager.calculate_position_size(10000, 100, 95), 20)

# Run the tests
unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestRiskManager))
