# 🎮 Replication Dynamics Game

A Streamlit application that simulates evolutionary game theory with 8 different automatons (strategies) competing over time. Watch as strategies evolve based on payoffs in a replication dynamics framework.

**Live Demo**: https://replication-game.streamlit.app

## Overview

This application models the evolution of 8 different strategies (automatons) playing against each other. The simulation uses replication dynamics where strategies with higher payoffs become more prevalent over time, creating a dynamic ecosystem of competing behaviors.

## Automatons (Strategies)

The 8 strategies competing in the game:

| Strategy | Type | Description |
|----------|------|-------------|
| **DOVE** | Peaceful | Passive cooperator |
| **HAWK** | Aggressive | Aggressive defector |
| **GRIM** | Retaliatory | Grudger (cooperates until betrayed) |
| **TIT-FOR-TAT** | Reciprocal | Mirrors opponent's previous move |
| **TAT-FOR-TIT** | Retaliatory | Retaliates for opponent's previous move |
| **TWEEDLEDUM** | Cooperative | Consistent cooperator |
| **TWEEDLEDEE** | Cooperative | Consistent cooperator |
| **TWEETYPIE** | Mixed | Aggressive mixed strategy |

## How It Works

1. **Initialization**: Each automaton starts with equal probability (1/8 ≈ 12.5%)
2. **Interaction**: In each period, automatons play against each other weighted by their current probabilities
3. **Payoff Calculation**: Each automaton receives payoffs based on the payoff matrix
4. **Reweighting**: Probabilities are updated based on payoffs:
   ```
   new_probability = current_probability × (payoff + adjustment)
   ```
   Probabilities are then normalized to sum to 1
5. **Evolution**: Over 100 periods (adjustable), you see which strategies prosper

## Features

- 🎯 **Interactive Simulation**: Adjust simulation periods (10-200)
- 📊 **Real-time Visualization**: Interactive charts showing strategy evolution
- 📈 **Multiple Views**:
  - Final distribution pie chart
  - Stacked area chart showing probability evolution
  - Line chart tracking payoff changes
- 📋 **Summary Statistics**: Dominant strategies, concentration metrics
- ⚡ **Fast Computation**: Instant results even for 200 periods

## Installation (Local)

```bash
git clone https://github.com/amaanib/Replication-Game.git
cd Replication-Game
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then visit `http://localhost:8501` in your browser.

## Running Online

No installation needed! Visit: **https://replication-game.streamlit.app**

## Outputs

The application displays:

1. **Final Probabilities Table**: Sorted by strategy prevalence
2. **Pie Chart**: Visual representation of final strategy distribution
3. **Stacked Area Chart**: Shows how probabilities evolved over time
4. **Payoff Chart**: Tracks average payoffs for each strategy
5. **Metrics**:
   - Most dominant strategy
   - Least common strategy
   - Concentration index (Herfindahl)

## Payoff Matrix

The payoff matrix defines the rewards each strategy receives when playing against every other strategy. Values are based on game theory principles of cooperation and defection.

Example interactions:
- DOVE vs DOVE = 1 point each
- HAWK vs DOVE = 3 points for HAWK, -0.5 for DOVE
- HAWK vs HAWK = 0 points each
- GRIM vs GRIM = 2 points each
- TIT-FOR-TAT vs TIT-FOR-TAT = 2 points each

## Technologies

- **Streamlit**: Web app framework
- **NumPy**: Numerical computations
- **Pandas**: Data handling
- **Plotly**: Interactive visualizations

## Project Structure

```
├── streamlit_app.py          # Main app (for Streamlit Cloud)
├── app_simple.py             # Simplified version
├── replication_dynamics.py    # Original version with enhanced UI
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore rules
```

## Usage Example

1. Open the app (locally or online)
2. Adjust "Simulation Periods" in the sidebar (default: 100)
3. Click **"🎮 Run Simulation"**
4. View results:
   - See which strategy becomes dominant
   - Track how probabilities change over time
   - Compare payoff trajectories

## Game Theory Background

This simulation implements **replication dynamics**, a fundamental concept in evolutionary game theory. Strategies that earn higher payoffs replicate more, while less successful strategies decline. Over time, the population evolves toward equilibrium configurations.

## License

MIT License - feel free to use and modify!

## Author

Created for exploring evolutionary game theory dynamics.

---

**Try it now**: https://replication-game.streamlit.app
