"""Equity calculation using Monte Carlo simulation."""

import random
from treys import Card
from poker_engine.calculations.hand_evaluator import HandEvaluator


class EquityCalculator:
    """Calculate equity using Monte Carlo simulation."""
    
    def __init__(self):
        """Initialize the equity calculator."""
        self.evaluator = HandEvaluator()
    
    def compute_equity(self, hero_hand, board, villain_range, iterations=40000):
        """
        Compute hero's equity against villain's range using Monte Carlo simulation.
        
        Args:
            hero_hand: List of 2 hero cards (treys integers)
            board: List of board cards (0-5 cards, treys integers)
            villain_range: List of villain hand combinations, each is [card1, card2]
            iterations: Number of Monte Carlo iterations (default: 40000)
            
        Returns:
            Float equity value (0.0-1.0)
        """
        if len(hero_hand) != 2:
            raise ValueError("Hero hand must contain exactly 2 cards")
        
        if len(board) > 5:
            raise ValueError("Board cannot have more than 5 cards")
        
        if not villain_range:
            raise ValueError("Villain range cannot be empty")
        
        # Filter out invalid villain hands (overlap with hero or board)
        valid_villain_hands = self._filter_valid_hands(villain_range, hero_hand, board)
        
        if not valid_villain_hands:
            # No valid hands in range, hero wins 100%
            return 1.0
        
        # Count wins, losses, and ties
        wins = 0
        losses = 0
        ties = 0
        
        # Get all used cards
        used_cards = set(hero_hand + board)
        
        for _ in range(iterations):
            # Randomly select villain hand from valid range
            villain_hand = random.choice(valid_villain_hands)
            
            # Check if villain hand overlaps with hero/board
            if any(card in used_cards for card in villain_hand):
                continue
            
            # Deal remaining board cards
            all_used = used_cards | set(villain_hand)
            final_board = self._deal_remaining_board(board, all_used)
            
            # Evaluate both hands
            hero_score = self.evaluator.evaluator.evaluate(final_board, hero_hand)
            villain_score = self.evaluator.evaluator.evaluate(final_board, villain_hand)
            
            # Compare (lower score is better in treys)
            if hero_score < villain_score:
                wins += 1
            elif hero_score > villain_score:
                losses += 1
            else:
                ties += 1
        
        total = wins + losses + ties
        if total == 0:
            return 0.0
        
        # Equity = wins + (ties / 2)
        equity = (wins + ties / 2) / total
        return equity
    
    def _filter_valid_hands(self, villain_range, hero_hand, board):
        """
        Filter out villain hands that overlap with hero hand or board.
        
        Args:
            villain_range: List of villain hand combinations
            hero_hand: Hero's cards
            board: Board cards
            
        Returns:
            List of valid villain hands
        """
        used_cards = set(hero_hand + board)
        valid_hands = []
        
        for hand in villain_range:
            if len(hand) != 2:
                continue
            # Check if hand overlaps with used cards
            if not any(card in used_cards for card in hand):
                valid_hands.append(hand)
        
        return valid_hands
    
    def _deal_remaining_board(self, current_board, used_cards):
        """
        Deal remaining board cards randomly.
        
        Args:
            current_board: Current board cards (0-5 cards)
            used_cards: Set of cards already used
            
        Returns:
            Complete board (5 cards)
        """
        if len(current_board) >= 5:
            return current_board
        
        # Generate all 52 cards
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['s', 'h', 'd', 'c']
        
        all_cards = []
        for rank in ranks:
            for suit in suits:
                try:
                    card = Card.new(rank + suit)
                    all_cards.append(card)
                except:
                    pass
        
        # Filter out used cards
        available_cards = [card for card in all_cards if card not in used_cards]
        
        # Shuffle and deal remaining cards
        random.shuffle(available_cards)
        remaining_needed = 5 - len(current_board)
        
        final_board = list(current_board) + available_cards[:remaining_needed]
        return final_board

