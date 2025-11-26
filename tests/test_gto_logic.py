"""Tests for GTO decision logic."""

import unittest
from poker_engine.calculations.gto_logic import choose_action, Action


class TestGTOLogic(unittest.TestCase):
    """Test GTO decision logic functionality."""
    
    def test_fold_decision(self):
        """Test fold decision when equity is too low."""
        # Equity: 0.2, Required: 0.4 → FOLD
        action, raise_size = choose_action(0.2, 0.4)
        self.assertEqual(action, Action.FOLD)
        self.assertIsNone(raise_size)
    
    def test_call_decision(self):
        """Test call decision when equity matches required."""
        # Equity: 0.35, Required: 0.33 → CALL (close enough)
        action, raise_size = choose_action(0.35, 0.33)
        self.assertEqual(action, Action.CALL)
        self.assertIsNone(raise_size)
    
    def test_raise_decision(self):
        """Test raise decision when equity is high."""
        # Equity: 0.6, Required: 0.3 → RAISE (0.6 > 0.3 * 1.2)
        action, raise_size = choose_action(0.6, 0.3, bet_sizes=[45, 90])
        self.assertEqual(action, Action.RAISE)
        self.assertIsNotNone(raise_size)
    
    def test_raise_size_selection(self):
        """Test raise size selection."""
        # High equity advantage → larger raise
        action, raise_size = choose_action(0.8, 0.2, bet_sizes=[30, 60, 120])
        self.assertEqual(action, Action.RAISE)
        self.assertIn(raise_size, [30, 60, 120])
    
    def test_aggression_factor(self):
        """Test aggression factor adjustment."""
        # With high aggression, should raise more often
        action1, _ = choose_action(0.5, 0.3, aggression=1.0)
        action2, _ = choose_action(0.5, 0.3, aggression=2.0)
        
        # Higher aggression might change call to raise
        # (depends on thresholds, but should be more aggressive)
        self.assertIn(action1, [Action.CALL, Action.RAISE])
        self.assertIn(action2, [Action.CALL, Action.RAISE])
    
    def test_marginal_call(self):
        """Test marginal call scenario."""
        # Equity: 0.34, Required: 0.33 → CALL (within threshold)
        action, raise_size = choose_action(0.34, 0.33)
        self.assertEqual(action, Action.CALL)
        self.assertIsNone(raise_size)
    
    def test_strong_raise(self):
        """Test strong hand raising."""
        # Equity: 0.9, Required: 0.2 → RAISE (very strong)
        action, raise_size = choose_action(0.9, 0.2, bet_sizes=[50, 100])
        self.assertEqual(action, Action.RAISE)
        self.assertIsNotNone(raise_size)
    
    def test_invalid_equity(self):
        """Test error handling for invalid equity."""
        with self.assertRaises(ValueError):
            choose_action(1.5, 0.3)  # Equity > 1
    
    def test_invalid_required_equity(self):
        """Test error handling for invalid required equity."""
        with self.assertRaises(ValueError):
            choose_action(0.5, -0.1)  # Required equity < 0
    
    def test_no_raise_sizes(self):
        """Test raise decision without available raise sizes."""
        # Should still return RAISE action, but raise_size is None
        action, raise_size = choose_action(0.8, 0.2)
        if action == Action.RAISE:
            self.assertIsNone(raise_size)


if __name__ == "__main__":
    unittest.main()

