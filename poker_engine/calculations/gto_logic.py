"""GTO decision logic for fold/call/raise decisions."""


class Action:
    """Action types."""
    FOLD = "FOLD"
    CALL = "CALL"
    RAISE = "RAISE"


def choose_action(equity, required_equity, bet_sizes=None, aggression=1.0, call_threshold=0.05, raise_threshold=1.2):
    """
    Choose optimal action based on equity vs required equity.
    
    Decision rules:
    - If equity < required_equity → FOLD
    - If equity ≈ required_equity (within threshold) → CALL
    - If equity > required_equity * raise_threshold → RAISE
    
    Args:
        equity: Hero's equity (0.0-1.0)
        required_equity: Required equity to call (0.0-1.0)
        bet_sizes: List of available raise sizes (optional)
        aggression: Aggression multiplier (default: 1.0, higher = more aggressive)
        call_threshold: Threshold for calling when equity is close to required (default: 0.05)
        raise_threshold: Multiplier above required equity to raise (default: 1.2)
        
    Returns:
        Tuple of (action, raise_size)
        - action: Action enum (FOLD, CALL, RAISE)
        - raise_size: Raise size if action is RAISE, None otherwise
    """
    if equity < 0 or equity > 1:
        raise ValueError("Equity must be between 0 and 1")
    if required_equity < 0 or required_equity > 1:
        raise ValueError("Required equity must be between 0 and 1")
    
    # Adjust thresholds based on aggression
    effective_raise_threshold = raise_threshold / aggression
    
    # Decision logic
    if equity < required_equity - call_threshold:
        # Equity is significantly below required → FOLD
        return Action.FOLD, None
    
    elif equity <= required_equity + call_threshold:
        # Equity is close to required → CALL
        return Action.CALL, None
    
    else:
        # Equity is above required → consider raising
        if equity >= required_equity * effective_raise_threshold:
            # Equity is significantly above required → RAISE
            raise_size = _choose_raise_size(equity, required_equity, bet_sizes)
            return Action.RAISE, raise_size
        else:
            # Equity is above required but not enough to raise → CALL
            return Action.CALL, None


def _choose_raise_size(equity, required_equity, bet_sizes):
    """
    Choose appropriate raise size from available options.
    
    Args:
        equity: Hero's equity
        required_equity: Required equity
        bet_sizes: List of available raise sizes
        
    Returns:
        Raise size (float) or None if no sizes provided
    """
    if not bet_sizes:
        return None
    
    # Sort bet sizes
    sorted_sizes = sorted(bet_sizes)
    
    # Calculate how much equity we have above required
    equity_advantage = equity / required_equity if required_equity > 0 else float('inf')
    
    # More equity advantage → larger raise size
    if equity_advantage >= 2.0:
        # Very strong, use largest raise size
        return sorted_sizes[-1]
    elif equity_advantage >= 1.5:
        # Strong, use medium-large raise size
        if len(sorted_sizes) >= 2:
            return sorted_sizes[-1] if len(sorted_sizes) == 2 else sorted_sizes[-2]
        return sorted_sizes[0]
    else:
        # Moderate advantage, use smaller raise size
        return sorted_sizes[0]

