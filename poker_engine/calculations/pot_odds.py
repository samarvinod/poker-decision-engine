"""Pot odds calculation."""


def pot_odds_required(pot, call_amount):
    """
    Calculate the required equity to make a call profitable.
    
    Formula: required_equity = call_amount / (pot + call_amount)
    
    Args:
        pot: Current pot size (before hero's call)
        call_amount: Amount hero needs to call
        
    Returns:
        Float representing required equity (0.0-1.0)
        
    Raises:
        ValueError: If pot or call_amount is negative, or both are zero
    """
    if pot < 0:
        raise ValueError("Pot size cannot be negative")
    if call_amount < 0:
        raise ValueError("Call amount cannot be negative")
    
    if pot == 0 and call_amount == 0:
        raise ValueError("Both pot and call amount cannot be zero")
    
    if call_amount == 0:
        # Free to call, no equity required
        return 0.0
    
    total_pot_after_call = pot + call_amount
    required_equity = call_amount / total_pot_after_call
    
    return required_equity


def pot_odds_ratio(pot, call_amount):
    """
    Calculate pot odds as a ratio (e.g., 3:1).
    
    Args:
        pot: Current pot size
        call_amount: Amount to call
        
    Returns:
        Tuple of (pot_odds_numerator, pot_odds_denominator)
        e.g., (3, 1) for 3:1 pot odds
    """
    if call_amount == 0:
        return (float('inf'), 1)
    
    ratio = pot / call_amount
    # Simplify to common ratio
    if ratio >= 1:
        return (int(ratio), 1)
    else:
        return (1, int(1 / ratio))

