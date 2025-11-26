"""Parse opponent ranges into hand combinations."""

from poker_engine.input.hand_parser import parse_card, HandParserError


class RangeParserError(Exception):
    """Custom exception for range parsing errors."""
    pass


# Card ranks for range parsing
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['s', 'h', 'd', 'c']


def _get_all_combos_of_hand(hand_str):
    """
    Get all combinations for a hand like "AK" (suited and offsuit).
    
    Args:
        hand_str: Hand string like "AK", "AKs", "AKo", "AA"
        
    Returns:
        List of [card1, card2] pairs as treys integers
    """
    if len(hand_str) < 2:
        raise RangeParserError(f"Invalid hand format: {hand_str}")
    
    rank1 = hand_str[0].upper()
    rank2 = hand_str[1].upper()
    
    if rank1 not in RANKS or rank2 not in RANKS:
        raise RangeParserError(f"Invalid ranks in hand: {hand_str}")
    
    # Check for suited/offsuit modifier
    is_suited = hand_str.endswith('s') and len(hand_str) == 3
    is_offsuit = hand_str.endswith('o') and len(hand_str) == 3
    
    combos = []
    
    if rank1 == rank2:
        # Pocket pair - all suit combinations
        for suit1 in SUITS:
            for suit2 in SUITS:
                if suit1 != suit2:
                    try:
                        card1 = parse_card(rank1 + suit1)
                        card2 = parse_card(rank2 + suit2)
                        combos.append([card1, card2])
                    except HandParserError:
                        pass
    elif is_suited:
        # Suited hands only
        for suit in SUITS:
            try:
                card1 = parse_card(rank1 + suit)
                card2 = parse_card(rank2 + suit)
                combos.append([card1, card2])
            except HandParserError:
                pass
    elif is_offsuit:
        # Offsuit hands only
        for suit1 in SUITS:
            for suit2 in SUITS:
                if suit1 != suit2:
                    try:
                        card1 = parse_card(rank1 + suit1)
                        card2 = parse_card(rank2 + suit2)
                        combos.append([card1, card2])
                    except HandParserError:
                        pass
    else:
        # Both suited and offsuit
        for suit1 in SUITS:
            for suit2 in SUITS:
                if suit1 != suit2:
                    try:
                        card1 = parse_card(rank1 + suit1)
                        card2 = parse_card(rank2 + suit2)
                        combos.append([card1, card2])
                    except HandParserError:
                        pass
        # Add suited
        for suit in SUITS:
            try:
                card1 = parse_card(rank1 + suit)
                card2 = parse_card(rank2 + suit)
                combos.append([card1, card2])
            except HandParserError:
                pass
    
    return combos


def _parse_range_notation(range_str):
    """
    Parse range notation like "JJ+", "22-99", "AK-AQ".
    
    Args:
        range_str: Range notation string
        
    Returns:
        List of hand strings
    """
    hands = []
    
    # Handle plus notation (e.g., "JJ+")
    if '+' in range_str:
        hand = range_str.replace('+', '')
        if len(hand) != 2:
            raise RangeParserError(f"Invalid plus notation: {range_str}")
        rank = hand[0].upper()
        if rank not in RANKS:
            raise RangeParserError(f"Invalid rank in plus notation: {range_str}")
        
        rank_idx = RANKS.index(rank)
        for i in range(rank_idx, len(RANKS)):
            hands.append(RANKS[i] + RANKS[i])  # Pocket pairs
        return hands
    
    # Handle range notation (e.g., "22-99", "AK-AQ")
    if '-' in range_str:
        parts = range_str.split('-')
        if len(parts) != 2:
            raise RangeParserError(f"Invalid range notation: {range_str}")
        
        start = parts[0].upper()
        end = parts[1].upper()
        
        # Pocket pair range
        if len(start) == 2 and len(end) == 2 and start[0] == start[1] and end[0] == end[1]:
            start_rank = start[0]
            end_rank = end[0]
            if start_rank not in RANKS or end_rank not in RANKS:
                raise RangeParserError(f"Invalid ranks in range: {range_str}")
            
            start_idx = RANKS.index(start_rank)
            end_idx = RANKS.index(end_rank)
            for i in range(start_idx, end_idx + 1):
                hands.append(RANKS[i] + RANKS[i])
            return hands
        
        # For now, just return the two hands (can be extended)
        return [start, end]
    
    return [range_str]


def parse_range(range_string):
    """
    Parse a range string into list of hand combinations.
    
    Supports:
    - Individual hands: "AK", "AKs", "AKo", "JJ"
    - Space-separated: "AK AQ JJ"
    - Plus notation: "JJ+" (pocket pairs and above)
    - Range notation: "22-99" (pocket pair range)
    
    Args:
        range_string: Range string in various formats
        
    Returns:
        List of [card1, card2] pairs as treys integers
    """
    if not range_string or range_string.strip() == "":
        return []
    
    # Split by spaces
    hand_strings = range_string.strip().split()
    
    all_combos = []
    seen_combos = set()
    
    for hand_str in hand_strings:
        # Handle range notation
        if '+' in hand_str or '-' in hand_str:
            expanded_hands = _parse_range_notation(hand_str)
            for expanded_hand in expanded_hands:
                combos = _get_all_combos_of_hand(expanded_hand)
                for combo in combos:
                    # Use sorted tuple to avoid duplicates
                    combo_key = tuple(sorted(combo))
                    if combo_key not in seen_combos:
                        seen_combos.add(combo_key)
                        all_combos.append(combo)
        else:
            combos = _get_all_combos_of_hand(hand_str)
            for combo in combos:
                combo_key = tuple(sorted(combo))
                if combo_key not in seen_combos:
                    seen_combos.add(combo_key)
                    all_combos.append(combo)
    
    return all_combos

