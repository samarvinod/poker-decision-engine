"""Hand strength evaluation using treys."""

from treys import Evaluator


class HandEvaluator:
    """Evaluate hand strength using treys."""
    
    def __init__(self):
        """Initialize the treys evaluator."""
        self.evaluator = Evaluator()
    
    def evaluate_hand(self, cards, board):
        """
        Evaluate hand strength.
        
        Args:
            cards: List of hero's hole cards (2 cards as treys integers)
            board: List of board cards (0-5 cards as treys integers)
            
        Returns:
            Tuple of (strength_score, hand_rank)
            - strength_score: Integer from treys (lower is better, 1 = royal flush)
            - hand_rank: String description of hand type
        """
        if len(cards) != 2:
            raise ValueError("Hero hand must contain exactly 2 cards")
        
        if len(board) > 5:
            raise ValueError("Board cannot have more than 5 cards")
        
        # Treys requires at least 5 cards to evaluate
        # For preflop (no board), we can't evaluate hand strength
        if len(board) == 0:
            raise ValueError("Cannot evaluate hand strength preflop. Treys requires at least 5 cards (2 hole + 3 board minimum)")
        
        # Evaluate the hand - treys evaluate takes (board, cards) as separate lists
        # It finds the best 5-card hand from all available cards
        score = self.evaluator.evaluate(board, cards)
        
        # Get hand class (rank) - use treys' built-in method
        hand_class = self.evaluator.get_rank_class(score)
        hand_rank = self.evaluator.class_to_string(hand_class)
        
        return score, hand_rank
    
    
    def compare_hands(self, hand1_cards, hand2_cards, board):
        """
        Compare two hands and determine winner.
        
        Args:
            hand1_cards: First hand (2 cards)
            hand2_cards: Second hand (2 cards)
            board: Board cards
            
        Returns:
            -1 if hand1 wins, 1 if hand2 wins, 0 if tie
        """
        score1 = self.evaluator.evaluate(board, hand1_cards)
        score2 = self.evaluator.evaluate(board, hand2_cards)
        
        if score1 < score2:
            return -1  # hand1 wins
        elif score1 > score2:
            return 1   # hand2 wins
        else:
            return 0   # tie

