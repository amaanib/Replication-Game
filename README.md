# Replication Dynamics Game Simulator

A Streamlit application that simulates replication dynamics with game theory automatons.

## Overview

This application models the evolution of 8 different strategies (automatons) playing against each other over 100 periods. The simulation uses replication dynamics where strategies with higher payoffs become more prevalent over time.

## Automatons

The following strategies are simulated:
- **DOVE**: Passive cooperator
- **HAWK**: Aggressive defector
- **GRIM**: Grudger strategy (cooperates until betrayed)
- **TIT-FOR-TAT**: Mirrors opponent's previous move
- **TAT-FOR-TIT**: Retaliates for opponent's previous move
- **TWEEDLEDUM**: Consistent cooperator
- **TWEEDLEDEE**: Consistent cooperator
- **TWEETYPIE**: Aggressive strategy

## How It Works

1. **Initialization**: Each automaton starts with equal probability (1/8)
2. **Interaction**: In each period, automatons play against each other weighted by their current probabilities
3. **Payoff Calculation**: Each automaton receives payoffs based on interactions (from the provided payoff matrix)
4. **Reweighting**: Probabilities are updated proportionally to payoffs using:
   - `new_probability = current_probability × (payoff + adjustment)`
   - Probabilities are then normalized to sum to 1
5. **Evolution**: After 100 periods, you see which strategies have prospered

## Installation

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run replication_dynamics.py
```

## Features

- **Interactive Simulation**: Adjust the number of periods (10-200)
- **Real-time Visualization**: See strategy probabilities evolve over time
- **Final Distribution**: Pie chart showing the final strategy composition
- **Payoff Evolution**: Track how average payoffs change for each strategy
- **Summary Statistics**: View the most dominant strategy and concentration metrics

## Outputs

The application generates:
1. **Final Probabilities Table**: Sorted by strategy prevalence
2. **Pie Chart**: Visual representation of final strategy distribution
3. **Stacked Area Chart**: Shows how probabilities evolved over 100 periods
4. **Payoff Chart**: Tracks average payoffs for each strategy over time
5. **Summary Metrics**: Concentration index and dominant strategies

## Payoff Matrix

The payoff matrix is based on the provided game theory data, representing what each automaton earns when playing against every other automaton.
