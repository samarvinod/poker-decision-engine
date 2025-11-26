"""Tests for hand evaluator."""

import unittest
from poker_engine.input.hand_parser import parse_hand, parse_board
from poker_engine.calculations.hand_evaluator import HandEvaluator


class TestHandEvaluator(unittest.TestCase):
    """Test hand evaluation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = HandEvaluator()
    
    def test_evaluate_preflop(self):
        """Test preflop hand evaluation."""
        # Test pocket aces - preflop evaluation not supported (needs board)
        aces = parse_hand("Ah As")
        with self.assertRaises(ValueError):
            self.evaluator.evaluate_hand(aces, [])
    
    def test_evaluate_flop(self):
        """Test postflop hand evaluation."""
        # Test pair on board
        hand = parse_hand("Ah Ks")
        board = parse_board("Ac 7d 2h")
        score, rank = self.evaluator.evaluate_hand(hand, board)
        self.assertEqual(rank, "Pair")
    
    def test_evaluate_straight(self):
        """Test straight evaluation."""
        hand = parse_hand("5h 6s")
        board = parse_board("7c 8d 9h")
        score, rank = self.evaluator.evaluate_hand(hand, board)
        self.assertEqual(rank, "Straight")
    
    def test_evaluate_flush(self):
        """Test flush evaluation."""
        hand = parse_hand("Ah 2h")
        board = parse_board("5h 7h 9h")
        score, rank = self.evaluator.evaluate_hand(hand, board)
        self.assertEqual(rank, "Flush")
    
    def test_compare_hands(self):
        """Test hand comparison."""
        hand1 = parse_hand("Ah As")
        hand2 = parse_hand("Kd Ks")
        board = parse_board("7c 8d 2h")
        
        result = self.evaluator.compare_hands(hand1, hand2, board)
        self.assertEqual(result, -1)  # Aces should win
    
    def test_invalid_hand_size(self):
        """Test error handling for invalid hand size."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate_hand([1], [])
    
    def test_invalid_board_size(self):
        """Test error handling for invalid board size."""
        hand = parse_hand("Ah As")
        board = [1, 2, 3, 4, 5, 6]  # Too many cards
        with self.assertRaises(ValueError):
            self.evaluator.evaluate_hand(hand, board)


if __name__ == "__main__":
    unittest.main()

