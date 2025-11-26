"""Main decision engine orchestrator."""

import argparse
from typing import List, Optional, Dict, Any
from poker_engine.input.hand_parser import parse_hand, parse_board, HandParserError
from poker_engine.input.range_parser import parse_range, RangeParserError
from poker_engine.calculations.hand_evaluator import HandEvaluator
from poker_engine.calculations.equity_calculator import EquityCalculator
from poker_engine.calculations.pot_odds import pot_odds_required
from poker_engine.calculations.gto_logic import choose_action, Action


class DecisionResult:
    """Result of a decision calculation."""
    
    def __init__(self, action, equity, required_equity, raise_size=None, explanation=""):
        self.action = action
        self.equity = equity
        self.required_equity = required_equity
        self.raise_size = raise_size
        self.explanation = explanation
    
    def to_dict(self):
        """Convert result to dictionary."""
        return {
            "action": self.action,
            "equity": self.equity,
            "required_equity": self.required_equity,
            "raise_size": self.raise_size,
            "explanation": self.explanation
        }
    
    def __str__(self):
        """Human-readable string representation."""
        equity_pct = self.equity * 100
        required_pct = self.required_equity * 100
        
        lines = [
            f"Recommended Action: {self.action}",
            f"Your Equity: {equity_pct:.1f}%",
            f"Required Equity: {required_pct:.1f}%",
        ]
        
        if self.action == Action.RAISE and self.raise_size:
            lines.append(f"Raise Size: {self.raise_size}")
        
        lines.append(f"\nExplanation: {self.explanation}")
        
        return "\n".join(lines)


class PokerDecisionEngine:
    """Main poker decision engine."""
    
    def __init__(self, equity_iterations=40000):
        """
        Initialize the decision engine.
        
        Args:
            equity_iterations: Number of Monte Carlo iterations for equity calculation
        """
        self.hand_evaluator = HandEvaluator()
        self.equity_calculator = EquityCalculator()
        self.equity_iterations = equity_iterations
    
    def make_decision(
        self,
        hero_hand: List[int],
        board: List[int],
        villain_range: List[List[int]],
        pot: float,
        to_call: float,
        raise_sizes: Optional[List[float]] = None,
        aggression: float = 1.0
    ) -> DecisionResult:
        """
        Make a decision based on game state.
        
        Args:
            hero_hand: Hero's hole cards (2 cards as treys integers)
            board: Board cards (0-5 cards as treys integers)
            villain_range: List of villain hand combinations
            pot: Current pot size
            to_call: Amount to call
            raise_sizes: Available raise sizes (optional)
            aggression: Aggression multiplier (default: 1.0)
            
        Returns:
            DecisionResult object with action and explanation
        """
        # Calculate equity
        equity = self.equity_calculator.compute_equity(
            hero_hand, board, villain_range, self.equity_iterations
        )
        
        # Calculate required equity (pot odds)
        required_equity = pot_odds_required(pot, to_call)
        
        # Choose action
        action, raise_size = choose_action(
            equity, required_equity, raise_sizes, aggression
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            action, equity, required_equity, raise_size
        )
        
        return DecisionResult(action, equity, required_equity, raise_size, explanation)
    
    def _generate_explanation(
        self, action, equity, required_equity, raise_size
    ) -> str:
        """Generate human-readable explanation for the decision."""
        equity_pct = equity * 100
        required_pct = required_equity * 100
        
        if action == Action.FOLD:
            return (
                f"You should fold because your equity ({equity_pct:.1f}%) "
                f"is below the required equity ({required_pct:.1f}%). "
                f"Calling would be unprofitable in the long run."
            )
        elif action == Action.CALL:
            if equity > required_equity:
                return (
                    f"You should call. Your equity ({equity_pct:.1f}%) "
                    f"exceeds the required equity ({required_pct:.1f}%), "
                    f"making this a profitable call."
                )
            else:
                return (
                    f"You should call. Your equity ({equity_pct:.1f}%) "
                    f"is close to the required equity ({required_pct:.1f}%). "
                    f"This is a marginal but acceptable call."
                )
        else:  # RAISE
            return (
                f"You should raise to {raise_size}. Your equity ({equity_pct:.1f}%) "
                f"is significantly higher than the required equity ({required_pct:.1f}%), "
                f"indicating your hand is strong enough to value bet."
            )


def parse_cli_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Poker Decision Engine - Get optimal poker decisions based on GTO principles"
    )
    
    parser.add_argument(
        "--hero-hand",
        required=True,
        help="Hero's hole cards (e.g., 'Ah Qs' or 'AhQs')"
    )
    
    parser.add_argument(
        "--board",
        default="",
        help="Board cards (e.g., '8c 7d 2h' or empty for preflop)"
    )
    
    parser.add_argument(
        "--villain-range",
        required=True,
        help="Villain's range (e.g., 'AK AQ JJ' or 'JJ+')"
    )
    
    parser.add_argument(
        "--pot",
        type=float,
        required=True,
        help="Current pot size"
    )
    
    parser.add_argument(
        "--to-call",
        type=float,
        required=True,
        help="Amount to call"
    )
    
    parser.add_argument(
        "--raise-sizes",
        nargs="+",
        type=float,
        help="Available raise sizes (e.g., '45 90')"
    )
    
    parser.add_argument(
        "--aggression",
        type=float,
        default=1.0,
        help="Aggression multiplier (default: 1.0, higher = more aggressive)"
    )
    
    parser.add_argument(
        "--iterations",
        type=int,
        default=40000,
        help="Number of Monte Carlo iterations for equity (default: 40000)"
    )
    
    return parser.parse_args()


def main():
    """Main CLI entry point."""
    args = parse_cli_args()
    
    try:
        # Parse inputs
        hero_hand = parse_hand(args.hero_hand)
        board = parse_board(args.board)
        villain_range = parse_range(args.villain_range)
        
        # Validate inputs
        if len(hero_hand) != 2:
            print("Error: Hero hand must contain exactly 2 cards")
            return 1
        
        if len(board) > 5:
            print("Error: Board cannot have more than 5 cards")
            return 1
        
        if not villain_range:
            print("Error: Villain range is empty or invalid")
            return 1
        
        # Create engine and make decision
        engine = PokerDecisionEngine(equity_iterations=args.iterations)
        result = engine.make_decision(
            hero_hand=hero_hand,
            board=board,
            villain_range=villain_range,
            pot=args.pot,
            to_call=args.to_call,
            raise_sizes=args.raise_sizes,
            aggression=args.aggression
        )
        
        # Print result
        print("\n" + "="*120)
        print(result)
        print("="*120 + "\n")
        
        return 0
        
    except HandParserError as e:
        print(f"Error parsing hand/board: {e}")
        return 1
    except RangeParserError as e:
        print(f"Error parsing villain range: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

