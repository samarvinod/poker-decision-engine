"""Parse card strings to treys-compatible format."""

from treys import Card


class HandParserError(Exception):
    """Custom exception for hand parsing errors."""
    pass


def parse_card(card_string):
    """
    Parse a single card string to treys format.
    
    Args:
        card_string: Card in format "Ah", "Qs", "Kd", "Jc" (rank + suit)
        
    Returns:
        Integer card value compatible with treys
        
    Raises:
        HandParserError: If card format is invalid
    """
    if not card_string or len(card_string) != 2:
        raise HandParserError(f"Invalid card format: {card_string}. Expected format: 'Ah', 'Qs', etc.")
    
    rank = card_string[0].upper()
    suit = card_string[1].lower()
    
    # Map rank to treys format
    rank_map = {
        '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
        '8': '8', '9': '9', 'T': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
    }
    
    if rank not in rank_map:
        raise HandParserError(f"Invalid rank: {rank}. Must be 2-9, T, J, Q, K, or A")
    
    # Map suit
    suit_map = {'s': 's', 'h': 'h', 'd': 'd', 'c': 'c'}
    if suit not in suit_map:
        raise HandParserError(f"Invalid suit: {suit}. Must be s, h, d, or c")
    
    # Create treys card string and convert to integer
    treys_string = rank_map[rank] + suit_map[suit]
    try:
        return Card.new(treys_string)
    except Exception as e:
        raise HandParserError(f"Failed to create card from {card_string}: {e}")


def parse_hand(hand_string):
    """
    Parse a hand string (space-separated cards) to list of treys card integers.
    
    Args:
        hand_string: Space-separated cards like "Ah Qs" or "AhQs"
        
    Returns:
        List of integer card values
        
    Raises:
        HandParserError: If hand format is invalid
    """
    if not hand_string:
        return []
    
    # Handle both space-separated and concatenated formats
    hand_string = hand_string.replace(' ', '')
    
    if len(hand_string) % 2 != 0:
        raise HandParserError(f"Invalid hand format: {hand_string}. Must have even number of characters")
    
    cards = []
    for i in range(0, len(hand_string), 2):
        card_str = hand_string[i:i+2]
        cards.append(parse_card(card_str))
    
    return cards


def parse_board(board_string):
    """
    Parse board cards string to list of treys card integers.
    
    Args:
        board_string: Space-separated cards like "8c 7d 2h" or empty string
        
    Returns:
        List of integer card values (0-5 cards)
        
    Raises:
        HandParserError: If board format is invalid
    """
    if not board_string or board_string.strip() == "":
        return []
    
    return parse_hand(board_string)

