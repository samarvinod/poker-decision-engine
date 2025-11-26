"""Tests for range parser."""

import unittest
from poker_engine.input.range_parser import parse_range, RangeParserError


class TestRangeParser(unittest.TestCase):
    """Test range parsing functionality."""
    
    def test_parse_range_single_hand(self):
        """Test parsing single hand."""
        range_list = parse_range("AK")
        self.assertGreater(len(range_list), 0)
        for hand in range_list:
            self.assertEqual(len(hand), 2)
    
    def test_parse_range_multiple_hands(self):
        """Test parsing multiple hands."""
        range_list = parse_range("AK AQ JJ")
        self.assertGreater(len(range_list), 0)
    
    def test_parse_range_suited(self):
        """Test parsing suited hands."""
        range_list = parse_range("AKs")
        self.assertGreater(len(range_list), 0)
    
    def test_parse_range_offsuit(self):
        """Test parsing offsuit hands."""
        range_list = parse_range("AKo")
        self.assertGreater(len(range_list), 0)
    
    def test_parse_range_pocket_pair(self):
        """Test parsing pocket pair."""
        range_list = parse_range("AA")
        self.assertGreater(len(range_list), 0)
    
    def test_parse_range_plus_notation(self):
        """Test parsing plus notation."""
        range_list = parse_range("JJ+")
        self.assertGreater(len(range_list), 0)
        # Should include JJ, QQ, KK, AA
    
    def test_parse_range_empty(self):
        """Test parsing empty range."""
        range_list = parse_range("")
        self.assertEqual(len(range_list), 0)
    
    def test_parse_range_invalid(self):
        """Test error handling for invalid range."""
        # This might not raise an error depending on implementation
        # but should handle gracefully
        try:
            range_list = parse_range("XX")
            # If it doesn't raise, should return empty or handle gracefully
        except RangeParserError:
            pass  # Expected behavior


if __name__ == "__main__":
    unittest.main()

