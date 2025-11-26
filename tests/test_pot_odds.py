"""Tests for pot odds calculation."""

import unittest
from poker_engine.calculations.pot_odds import pot_odds_required, pot_odds_ratio


class TestPotOdds(unittest.TestCase):
    """Test pot odds calculation functionality."""
    
    def test_pot_odds_basic(self):
        """Test basic pot odds calculation."""
        # Pot: 100, Call: 50
        # Required = 50 / (100 + 50) = 50/150 = 0.333
        required = pot_odds_required(100, 50)
        self.assertAlmostEqual(required, 0.333, places=2)
    
    def test_pot_odds_even_money(self):
        """Test even money pot odds."""
        # Pot: 50, Call: 50
        # Required = 50 / (50 + 50) = 0.5
        required = pot_odds_required(50, 50)
        self.assertAlmostEqual(required, 0.5, places=2)
    
    def test_pot_odds_large_pot(self):
        """Test pot odds with large pot."""
        # Pot: 200, Call: 50
        # Required = 50 / (200 + 50) = 50/250 = 0.2
        required = pot_odds_required(200, 50)
        self.assertAlmostEqual(required, 0.2, places=2)
    
    def test_pot_odds_small_call(self):
        """Test pot odds with small call."""
        # Pot: 100, Call: 10
        # Required = 10 / (100 + 10) = 10/110 ≈ 0.091
        required = pot_odds_required(100, 10)
        self.assertAlmostEqual(required, 0.091, places=2)
    
    def test_pot_odds_free_call(self):
        """Test pot odds with free call (call = 0)."""
        required = pot_odds_required(100, 0)
        self.assertEqual(required, 0.0)
    
    def test_pot_odds_negative_pot(self):
        """Test error handling for negative pot."""
        with self.assertRaises(ValueError):
            pot_odds_required(-10, 50)
    
    def test_pot_odds_negative_call(self):
        """Test error handling for negative call."""
        with self.assertRaises(ValueError):
            pot_odds_required(100, -10)
    
    def test_pot_odds_both_zero(self):
        """Test error handling for both pot and call being zero."""
        with self.assertRaises(ValueError):
            pot_odds_required(0, 0)
    
    def test_pot_odds_ratio(self):
        """Test pot odds ratio calculation."""
        # Pot: 150, Call: 50 → 3:1
        num, den = pot_odds_ratio(150, 50)
        self.assertEqual(num, 3)
        self.assertEqual(den, 1)
    
    def test_pot_odds_ratio_free_call(self):
        """Test pot odds ratio for free call."""
        num, den = pot_odds_ratio(100, 0)
        self.assertEqual(num, float('inf'))
        self.assertEqual(den, 1)


if __name__ == "__main__":
    unittest.main()

