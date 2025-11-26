"""Tests for hand parser."""

import unittest
from poker_engine.input.hand_parser import parse_card, parse_hand, parse_board, HandParserError


class TestHandParser(unittest.TestCase):
    """Test hand parsing functionality."""
    
    def test_parse_card_valid(self):
        """Test parsing valid cards."""
        card = parse_card("Ah")
        self.assertIsInstance(card, int)
        
        card = parse_card("Qs")
        self.assertIsInstance(card, int)
    
    def test_parse_card_invalid_format(self):
        """Test error handling for invalid card format."""
        with self.assertRaises(HandParserError):
            parse_card("A")
        
        with self.assertRaises(HandParserError):
            parse_card("AhQ")
    
    def test_parse_card_invalid_rank(self):
        """Test error handling for invalid rank."""
        with self.assertRaises(HandParserError):
            parse_card("Xh")
    
    def test_parse_card_invalid_suit(self):
        """Test error handling for invalid suit."""
        with self.assertRaises(HandParserError):
            parse_card("Ax")
    
    def test_parse_hand_space_separated(self):
        """Test parsing space-separated hand."""
        hand = parse_hand("Ah Qs")
        self.assertEqual(len(hand), 2)
    
    def test_parse_hand_concatenated(self):
        """Test parsing concatenated hand."""
        hand = parse_hand("AhQs")
        self.assertEqual(len(hand), 2)
    
    def test_parse_hand_empty(self):
        """Test parsing empty hand."""
        hand = parse_hand("")
        self.assertEqual(len(hand), 0)
    
    def test_parse_board_empty(self):
        """Test parsing empty board."""
        board = parse_board("")
        self.assertEqual(len(board), 0)
    
    def test_parse_board_flop(self):
        """Test parsing flop."""
        board = parse_board("8c 7d 2h")
        self.assertEqual(len(board), 3)
    
    def test_parse_board_turn(self):
        """Test parsing turn."""
        board = parse_board("8c 7d 2h Kh")
        self.assertEqual(len(board), 4)
    
    def test_parse_board_river(self):
        """Test parsing river."""
        board = parse_board("8c 7d 2h Kh 9s")
        self.assertEqual(len(board), 5)


if __name__ == "__main__":
    unittest.main()

