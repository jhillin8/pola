# SB 988 Freelancer-Client Ecosystem Simulator

A comprehensive simulation laboratory for modeling freelancer-client relationship dynamics and SB 988 compliance scenarios.

## Overview

This simulator provides a modular, extensible framework for analyzing the economic and behavioral impacts of California's SB 988 legislation on the freelance economy. The system can model complex interactions between freelancers, clients, contracts, and regulatory compliance mechanisms.

## Architecture

### Core Components

- **Data Generators**: Synthetic data creation for freelancers, clients, contracts, and transactions
- **Behavioral Models**: Decision-making pattern simulation engines
- **Economic Analysis**: Compliance cost impact assessment tools
- **Regulatory Scenarios**: Framework for testing different policy configurations
- **Agent-Based Modeling**: Network effect simulation system
- **Monte Carlo Simulation**: Stochastic outcome prediction capabilities
- **Policy Models**: Regulatory impact prediction engines
- **Visualization**: Results analysis and presentation tools

### Directory Structure

```
sb988_simulator/
├── src/
│   ├── core/                 # Core simulation engine
│   ├── data_generators/      # Synthetic data creation
│   ├── behavioral_models/    # Decision-making models
│   ├── economic_analysis/    # Cost impact analysis
│   ├── regulatory_scenarios/ # Compliance scenario testing
│   ├── agent_based/         # Network effect modeling
│   ├── monte_carlo/         # Stochastic simulations
│   ├── policy_models/       # Policy impact prediction
│   ├── visualization/       # Results visualization
│   └── config/              # Configuration management
├── tests/                   # Unit and integration tests
├── docs/                    # Documentation
├── data/                    # Data storage
├── notebooks/               # Jupyter analysis notebooks
├── scripts/                 # Utility scripts
└── results/                 # Simulation outputs
```

## Technology Stack

- **Python 3.11+**: Primary language for simulation logic
- **NumPy/Pandas**: Data manipulation and analysis
- **SciPy**: Statistical and scientific computing
- **NetworkX**: Graph-based modeling for relationship networks
- **Matplotlib/Plotly**: Visualization and charting
- **Pydantic**: Data validation and settings management
- **SQLite**: Local data persistence
- **Jupyter**: Interactive analysis and prototyping

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Configure simulation parameters in `src/config/settings.py`
3. Generate synthetic data: `python scripts/generate_data.py`
4. Run simulations: `python scripts/run_simulation.py`
5. Analyze results in Jupyter notebooks

## Key Features

- **Modular Design**: Each component can be used independently or combined
- **Extensible Framework**: Easy to add new models and scenarios
- **Scalable Architecture**: Handles large numbers of simulated entities
- **Configurable Scenarios**: Test different regulatory configurations
- **Rich Visualization**: Multiple output formats for analysis
- **Statistical Rigor**: Monte Carlo methods for uncertainty quantification

## License

This is a local development project for research and analysis purposes.