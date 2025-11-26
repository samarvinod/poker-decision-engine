# Poker Decision Engine

A Texas Hold'em decision engine that evaluates game situations and recommends optimal actions (fold/call/raise) based on hand equity, pot odds, and GTO (Game Theory Optimal) principles.

## Features

- **Hand Evaluation**: Evaluate hand strength using the treys library
- **Equity Calculation**: Monte Carlo simulation to calculate equity vs opponent ranges
- **Pot Odds**: Calculate required equity based on pot size and bet amounts
- **GTO Decision Logic**: Make optimal decisions using equity vs pot odds analysis
- **CLI Interface**: Command-line tool for quick decision making
- **Python API**: Programmatic interface for integration into other applications

## Installation

### Prerequisites

- Python 3.10 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/samarvinod/poker-decision-engine.git
cd poker-decision-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install the package in development mode:
```bash
pip install -e .
```

## Usage

### Command-Line Interface

The CLI provides a simple way to get poker decisions:

```bash
poker-engine \
  --hero-hand "Ah Qs" \
  --board "8c 7d 2h" \
  --villain-range "AK AQ JJ" \
  --pot 45 \
  --to-call 15 \
  --raise-sizes 45 90
```

#### Arguments

- `--hero-hand`: Your hole cards (e.g., "Ah Qs" or "AhQs")
- `--board`: Board cards (e.g., "8c 7d 2h" or empty for preflop)
- `--villain-range`: Opponent's range (e.g., "AK AQ JJ" or "JJ+")
- `--pot`: Current pot size
- `--to-call`: Amount you need to call
- `--raise-sizes`: (Optional) Available raise sizes
- `--aggression`: (Optional) Aggression multiplier (default: 1.0)
- `--iterations`: (Optional) Monte Carlo iterations (default: 40000)

#### Example Output

```
============================================================
Recommended Action: RAISE
Your Equity: 45.2%
Required Equity: 25.0%
Raise Size: 90

Explanation: You should raise to 90. Your equity (45.2%) is significantly higher than the required equity (25.0%), indicating your hand is strong enough to value bet.
============================================================
```

### Python API

You can also use the engine programmatically:

```python
from poker_engine.input.hand_parser import parse_hand, parse_board
from poker_engine.input.range_parser import parse_range
from poker_engine.engine.decision_engine import PokerDecisionEngine

# Parse inputs
hero_hand = parse_hand("Ah Qs")
board = parse_board("8c 7d 2h")
villain_range = parse_range("AK AQ JJ")

# Create engine
engine = PokerDecisionEngine(equity_iterations=40000)

# Make decision
result = engine.make_decision(
    hero_hand=hero_hand,
    board=board,
    villain_range=villain_range,
    pot=45,
    to_call=15,
    raise_sizes=[45, 90]
)

# Access results
print(result.action)  # "RAISE"
print(result.equity)  # 0.452
print(result.required_equity)  # 0.25
print(result.raise_size)  # 90
print(result.explanation)  # Human-readable explanation
```

## Input Formats

### Card Format

Cards are specified as rank + suit:
- **Ranks**: 2-9, T (ten), J, Q, K, A
- **Suits**: s (spades), h (hearts), d (diamonds), c (clubs)

Examples: `"Ah"`, `"Qs"`, `"Kd"`, `"Jc"`

### Range Format

Villain ranges can be specified in several ways:

- **Individual hands**: `"AK"`, `"AKs"` (suited), `"AKo"` (offsuit), `"JJ"` (pocket pair)
- **Multiple hands**: `"AK AQ JJ"` (space-separated)
- **Plus notation**: `"JJ+"` (pocket pairs JJ and above)
- **Range notation**: `"22-99"` (pocket pair range)

## Architecture

```
poker_engine/
├── input/
│   ├── hand_parser.py      # Parse card strings to treys format
│   └── range_parser.py     # Parse opponent ranges
├── calculations/
│   ├── hand_evaluator.py   # Hand strength evaluation
│   ├── equity_calculator.py # Monte Carlo equity calculation
│   ├── pot_odds.py         # Pot odds calculation
│   └── gto_logic.py        # Decision rules
└── engine/
    └── decision_engine.py  # Main orchestrator
```

## API Reference

### `PokerDecisionEngine`

Main decision engine class.

#### Methods

##### `__init__(equity_iterations=40000)`

Initialize the engine.

- `equity_iterations`: Number of Monte Carlo iterations for equity calculation

##### `make_decision(hero_hand, board, villain_range, pot, to_call, raise_sizes=None, aggression=1.0)`

Make a decision based on game state.

**Parameters:**
- `hero_hand`: List of 2 hole cards (treys integers)
- `board`: List of board cards (0-5 cards, treys integers)
- `villain_range`: List of villain hand combinations
- `pot`: Current pot size
- `to_call`: Amount to call
- `raise_sizes`: (Optional) Available raise sizes
- `aggression`: (Optional) Aggression multiplier

**Returns:** `DecisionResult` object

### `DecisionResult`

Result object containing decision information.

**Attributes:**
- `action`: Action taken (FOLD, CALL, or RAISE)
- `equity`: Hero's equity (0.0-1.0)
- `required_equity`: Required equity to call (0.0-1.0)
- `raise_size`: Raise size if action is RAISE, None otherwise
- `explanation`: Human-readable explanation

**Methods:**
- `to_dict()`: Convert result to dictionary
- `__str__()`: Human-readable string representation

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

Or run individual test files:

```bash
python -m unittest tests.test_hand_evaluator
python -m unittest tests.test_equity_calculator
python -m unittest tests.test_pot_odds
python -m unittest tests.test_gto_logic
python -m unittest tests.test_decision_engine
```

## How It Works

1. **Input Parsing**: Converts user-friendly card strings to internal treys format
2. **Hand Evaluation**: Evaluates hand strength using treys evaluator
3. **Equity Calculation**: Runs Monte Carlo simulation (default: 40,000 iterations) to estimate equity vs opponent's range
4. **Pot Odds**: Calculates required equity using formula: `call_amount / (pot + call_amount)`
5. **Decision Logic**: Compares equity to required equity:
   - If `equity < required_equity` → **FOLD**
   - If `equity ≈ required_equity` → **CALL**
   - If `equity > required_equity * threshold` → **RAISE**
6. **Output**: Returns action with explanation

## Examples

### Preflop Decision

```bash
poker-engine \
  --hero-hand "Ah As" \
  --board "" \
  --villain-range "AK AQ JJ" \
  --pot 100 \
  --to-call 50
```

### Postflop Decision with Raise Sizes

```bash
poker-engine \
  --hero-hand "Ah Kh" \
  --board "Qh Jh Th" \
  --villain-range "AK" \
  --pot 200 \
  --to-call 100 \
  --raise-sizes 300 400
```

### Using Aggression Factor

```bash
poker-engine \
  --hero-hand "Ah Qs" \
  --board "8c 7d 2h" \
  --villain-range "AK AQ" \
  --pot 50 \
  --to-call 25 \
  --aggression 1.5
```

## Limitations

- MVP version uses simplified GTO logic (not a full solver)
- Equity calculation uses Monte Carlo simulation (approximate, not exact)
- Range parsing supports basic notation (can be extended)
- No opponent modeling or multi-street analysis

## Future Enhancements

- Full CFR (Counterfactual Regret Minimization) solver
- Opponent modeling and dynamic range adjustment
- Multi-street analysis
- Preflop GTO tables integration
- GUI application
- Neural network-based equity estimation

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Author

[Add author information here]
