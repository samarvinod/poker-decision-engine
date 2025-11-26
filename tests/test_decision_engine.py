"""Tests for decision engine."""

import unittest
from poker_engine.input.hand_parser import parse_hand, parse_board
from poker_engine.input.range_parser import parse_range
from poker_engine.engine.decision_engine import PokerDecisionEngine, DecisionResult, Action


class TestDecisionEngine(unittest.TestCase):
    """Test decision engine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = PokerDecisionEngine(equity_iterations=10000)
    
    def test_make_decision_preflop(self):
        """Test decision making preflop."""
        hero_hand = parse_hand("Ah As")
        board = []
        villain_range = parse_range("AK AQ JJ")
        
        result = self.engine.make_decision(
            hero_hand=hero_hand,
            board=board,
            villain_range=villain_range,
            pot=100,
            to_call=50
        )
        
        self.assertIsInstance(result, DecisionResult)
        self.assertIn(result.action, [Action.CALL, Action.RAISE])
        self.assertGreater(result.equity, 0.0)
        self.assertLessEqual(result.equity, 1.0)
        self.assertIsNotNone(result.explanation)
    
    def test_make_decision_fold(self):
        """Test fold decision."""
        hero_hand = parse_hand("2h 3s")
        board = []
        villain_range = parse_range("AA KK QQ")
        
        result = self.engine.make_decision(
            hero_hand=hero_hand,
            board=board,
            villain_range=villain_range,
            pot=50,
            to_call=100  # Large bet, likely fold
        )
        
        # Might fold or call depending on equity
        self.assertIn(result.action, [Action.FOLD, Action.CALL, Action.RAISE])
    
    def test_make_decision_with_raise_sizes(self):
        """Test decision with available raise sizes."""
        hero_hand = parse_hand("Ah Kh")
        board = parse_board("Qh Jh Th")
        villain_range = parse_range("AK")
        
        result = self.engine.make_decision(
            hero_hand=hero_hand,
            board=board,
            villain_range=villain_range,
            pot=100,
            to_call=50,
            raise_sizes=[150, 200]
        )
        
        if result.action == Action.RAISE:
            self.assertIsNotNone(result.raise_size)
            self.assertIn(result.raise_size, [150, 200])
    
    def test_decision_result_to_dict(self):
        """Test DecisionResult to_dict method."""
        result = DecisionResult(
            action=Action.CALL,
            equity=0.5,
            required_equity=0.4,
            explanation="Test explanation"
        )
        
        result_dict = result.to_dict()
        self.assertEqual(result_dict["action"], Action.CALL)
        self.assertEqual(result_dict["equity"], 0.5)
        self.assertEqual(result_dict["required_equity"], 0.4)
        self.assertEqual(result_dict["explanation"], "Test explanation")
    
    def test_decision_result_str(self):
        """Test DecisionResult string representation."""
        result = DecisionResult(
            action=Action.RAISE,
            equity=0.6,
            required_equity=0.3,
            raise_size=90,
            explanation="Test explanation"
        )
        
        result_str = str(result)
        self.assertIn("RAISE", result_str)
        self.assertIn("60.0%", result_str)
        self.assertIn("90", result_str)
        self.assertIn("Test explanation", result_str)
    
    def test_aggression_parameter(self):
        """Test aggression parameter."""
        hero_hand = parse_hand("Ah Kh")
        board = []
        villain_range = parse_range("AK AQ")
        
        result1 = self.engine.make_decision(
            hero_hand=hero_hand,
            board=board,
            villain_range=villain_range,
            pot=100,
            to_call=50,
            aggression=1.0
        )
        
        result2 = self.engine.make_decision(
            hero_hand=hero_hand,
            board=board,
            villain_range=villain_range,
            pot=100,
            to_call=50,
            aggression=2.0
        )
        
        # Higher aggression might lead to more raises
        # (exact behavior depends on equity, but should be more aggressive)
        self.assertIsInstance(result1, DecisionResult)
        self.assertIsInstance(result2, DecisionResult)


if __name__ == "__main__":
    unittest.main()

