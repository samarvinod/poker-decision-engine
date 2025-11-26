"""Tests for equity calculator."""

import unittest
from poker_engine.input.hand_parser import parse_hand, parse_board
from poker_engine.input.range_parser import parse_range
from poker_engine.calculations.equity_calculator import EquityCalculator


class TestEquityCalculator(unittest.TestCase):
    """Test equity calculation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calculator = EquityCalculator()
    
    def test_equity_preflop_aces_vs_range(self):
        """Test equity of pocket aces vs a range."""
        hero_hand = parse_hand("Ah As")
        board = []
        villain_range = parse_range("AK AQ JJ")
        
        equity = self.calculator.compute_equity(
            hero_hand, board, villain_range, iterations=10000
        )
        
        # Aces should have high equity
        self.assertGreater(equity, 0.7)
        self.assertLessEqual(equity, 1.0)
    
    def test_equity_preflop_weak_hand(self):
        """Test equity of weak hand vs strong range."""
        hero_hand = parse_hand("2h 3s")
        board = []
        villain_range = parse_range("AA KK QQ")
        
        equity = self.calculator.compute_equity(
            hero_hand, board, villain_range, iterations=10000
        )
        
        # Weak hand should have low equity
        self.assertLess(equity, 0.3)
        self.assertGreaterEqual(equity, 0.0)
    
    def test_equity_postflop(self):
        """Test equity calculation on flop."""
        hero_hand = parse_hand("Ah Kh")
        board = parse_board("Qh Jh Th")
        villain_range = parse_range("AA KK")
        
        equity = self.calculator.compute_equity(
            hero_hand, board, villain_range, iterations=10000
        )
        
        # Flush should have high equity
        self.assertGreater(equity, 0.5)
    
    def test_equity_empty_range(self):
        """Test error handling for empty range."""
        hero_hand = parse_hand("Ah As")
        board = []
        villain_range = []
        
        with self.assertRaises(ValueError):
            self.calculator.compute_equity(hero_hand, board, villain_range)
    
    def test_equity_invalid_hand(self):
        """Test error handling for invalid hand."""
        hero_hand = [1]  # Invalid hand size
        board = []
        villain_range = parse_range("AK")
        
        with self.assertRaises(ValueError):
            self.calculator.compute_equity(hero_hand, board, villain_range)
    
    def test_equity_invalid_board(self):
        """Test error handling for invalid board."""
        hero_hand = parse_hand("Ah As")
        board = [1, 2, 3, 4, 5, 6]  # Too many cards
        villain_range = parse_range("AK")
        
        with self.assertRaises(ValueError):
            self.calculator.compute_equity(hero_hand, board, villain_range)


if __name__ == "__main__":
    unittest.main()

