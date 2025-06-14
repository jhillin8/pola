"""
Core simulation engine for the SB 988 compliance simulator.

This module provides the main simulation orchestration logic that coordinates
all the different modeling components.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
import logging
from dataclasses import dataclass
import numpy as np

from .entities import Freelancer, Client, Contract, Transaction, MarketSnapshot
from .scenario import Scenario
from .metrics import MetricsCollector


@dataclass
class SimulationConfig:
    """Configuration for simulation runs."""
    
    # Time parameters
    start_date: datetime
    end_date: datetime
    time_step: timedelta = timedelta(days=1)
    
    # Population parameters
    initial_freelancers: int = 1000
    initial_clients: int = 500
    
    # Market parameters
    market_volatility: float = 0.1
    regulatory_enforcement_level: float = 0.5
    
    # Behavioral parameters
    agent_interaction_probability: float = 0.1
    contract_formation_rate: float = 0.05
    
    # Economic parameters
    base_hourly_rate: float = 50.0
    inflation_rate: float = 0.03
    
    # Compliance parameters
    sb988_enforcement_date: Optional[datetime] = None
    compliance_grace_period: int = 90  # days
    
    # Simulation parameters
    random_seed: Optional[int] = None
    max_iterations: int = 10000
    convergence_threshold: float = 0.001


class SimulationEngine:
    """
    Main simulation engine that orchestrates the entire ecosystem model.
    
    This class coordinates data generation, behavioral modeling, economic analysis,
    and regulatory scenario testing to produce comprehensive simulation results.
    """
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.current_time = config.start_date
        
        # Core entities
        self.freelancers: Dict[str, Freelancer] = {}
        self.clients: Dict[str, Client] = {}
        self.contracts: Dict[str, Contract] = {}
        self.transactions: List[Transaction] = []
        
        # Simulation state
        self.market_snapshots: List[MarketSnapshot] = []
        self.metrics_collector = MetricsCollector()
        self.scenarios: List[Scenario] = []
        
        # Behavioral models (to be injected)
        self.freelancer_behavior_model: Optional[Callable] = None
        self.client_behavior_model: Optional[Callable] = None
        self.market_dynamics_model: Optional[Callable] = None
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize random number generator
        if config.random_seed:
            np.random.seed(config.random_seed)
    
    def add_scenario(self, scenario: Scenario) -> None:
        """Add a regulatory scenario to test."""
        self.scenarios.append(scenario)
    
    def set_behavioral_models(self, 
                            freelancer_model: Callable = None,
                            client_model: Callable = None,
                            market_model: Callable = None) -> None:
        """Inject behavioral models into the simulation."""
        if freelancer_model:
            self.freelancer_behavior_model = freelancer_model
        if client_model:
            self.client_behavior_model = client_model
        if market_model:
            self.market_dynamics_model = market_model
    
    def initialize_population(self) -> None:
        """Initialize the starting population of freelancers and clients."""
        self.logger.info("Initializing simulation population...")
        
        # This will be implemented with synthetic data generators
        # For now, create placeholder logic
        pass
    
    def step(self) -> None:
        """Execute one simulation time step."""
        self.logger.debug(f"Executing simulation step for {self.current_time}")
        
        # 1. Update market conditions
        self._update_market_conditions()
        
        # 2. Execute agent behaviors
        self._execute_agent_behaviors()
        
        # 3. Process contract lifecycle
        self._process_contracts()
        
        # 4. Apply regulatory scenarios
        self._apply_regulatory_scenarios()
        
        # 5. Collect metrics
        self._collect_step_metrics()
        
        # 6. Advance time
        self.current_time += self.config.time_step
    
    def run(self) -> Dict[str, Any]:
        """Run the complete simulation."""
        self.logger.info(f"Starting simulation from {self.config.start_date} to {self.config.end_date}")
        
        # Initialize
        self.initialize_population()
        
        # Main simulation loop
        iteration = 0
        while (self.current_time <= self.config.end_date and 
               iteration < self.config.max_iterations):
            
            self.step()
            iteration += 1
            
            # Check for convergence if needed
            if self._check_convergence():
                self.logger.info(f"Simulation converged after {iteration} iterations")
                break
        
        self.logger.info(f"Simulation completed after {iteration} iterations")
        
        # Generate final results
        return self._generate_results()
    
    def _update_market_conditions(self) -> None:
        """Update overall market conditions for this time step."""
        if self.market_dynamics_model:
            # Apply market dynamics model
            market_state = self.market_dynamics_model(
                freelancers=self.freelancers,
                clients=self.clients,
                contracts=self.contracts,
                current_time=self.current_time
            )
        
        # Create market snapshot
        snapshot = MarketSnapshot(
            timestamp=self.current_time,
            total_freelancers=len(self.freelancers),
            total_clients=len(self.clients),
            active_contracts=len([c for c in self.contracts.values() 
                                if c.status.value == "active"]),
            total_transaction_volume=sum(t.amount for t in self.transactions
                                       if t.transaction_date.date() == self.current_time.date()),
            average_hourly_rate=self._calculate_average_hourly_rate(),
            compliance_rate=self._calculate_compliance_rate()
        )
        
        self.market_snapshots.append(snapshot)
    
    def _execute_agent_behaviors(self) -> None:
        """Execute behavioral models for all agents."""
        # Execute freelancer behaviors
        if self.freelancer_behavior_model:
            for freelancer in self.freelancers.values():
                self.freelancer_behavior_model(
                    freelancer=freelancer,
                    market_state=self.market_snapshots[-1] if self.market_snapshots else None,
                    available_clients=list(self.clients.values()),
                    current_time=self.current_time
                )
        
        # Execute client behaviors
        if self.client_behavior_model:
            for client in self.clients.values():
                self.client_behavior_model(
                    client=client,
                    market_state=self.market_snapshots[-1] if self.market_snapshots else None,
                    available_freelancers=list(self.freelancers.values()),
                    current_time=self.current_time
                )
    
    def _process_contracts(self) -> None:
        """Process contract lifecycle events."""
        for contract in self.contracts.values():
            # Update contract status based on dates and conditions
            if (contract.end_date and 
                self.current_time.date() > contract.end_date and
                contract.status.value == "active"):
                contract.status = contract.status.COMPLETED
    
    def _apply_regulatory_scenarios(self) -> None:
        """Apply active regulatory scenarios to the simulation."""
        for scenario in self.scenarios:
            if scenario.is_active(self.current_time):
                scenario.apply(
                    freelancers=self.freelancers,
                    clients=self.clients,
                    contracts=self.contracts,
                    current_time=self.current_time
                )
    
    def _collect_step_metrics(self) -> None:
        """Collect metrics for this simulation step."""
        self.metrics_collector.collect_step_metrics(
            freelancers=self.freelancers,
            clients=self.clients,
            contracts=self.contracts,
            transactions=self.transactions,
            current_time=self.current_time
        )
    
    def _check_convergence(self) -> bool:
        """Check if the simulation has converged to a steady state."""
        # Simple convergence check based on recent market snapshots
        if len(self.market_snapshots) < 10:
            return False
        
        recent_snapshots = self.market_snapshots[-10:]
        compliance_rates = [s.compliance_rate for s in recent_snapshots]
        
        # Check if compliance rate has stabilized
        variance = np.var(compliance_rates)
        return variance < self.config.convergence_threshold
    
    def _calculate_average_hourly_rate(self) -> float:
        """Calculate the current average hourly rate across all freelancers."""
        if not self.freelancers:
            return 0.0
        
        rates = [float(f.hourly_rate) for f in self.freelancers.values()]
        return np.mean(rates)
    
    def _calculate_compliance_rate(self) -> float:
        """Calculate the current compliance rate across all contracts."""
        if not self.contracts:
            return 0.0
        
        compliant_contracts = sum(1 for c in self.contracts.values() 
                                if c.sb988_compliant.value == "compliant")
        return compliant_contracts / len(self.contracts)
    
    def _generate_results(self) -> Dict[str, Any]:
        """Generate comprehensive simulation results."""
        return {
            'config': self.config,
            'execution_summary': {
                'start_time': self.config.start_date,
                'end_time': self.current_time,
                'total_steps': len(self.market_snapshots),
                'final_population': {
                    'freelancers': len(self.freelancers),
                    'clients': len(self.clients),
                    'contracts': len(self.contracts),
                    'transactions': len(self.transactions)
                }
            },
            'market_evolution': self.market_snapshots,
            'metrics': self.metrics_collector.get_summary(),
            'scenario_results': [s.get_results() for s in self.scenarios],
            'entities': {
                'freelancers': list(self.freelancers.values()),
                'clients': list(self.clients.values()),
                'contracts': list(self.contracts.values()),
                'transactions': self.transactions
            }
        }