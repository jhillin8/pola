"""
Core simulation engine for the SB 988 compliance simulator.

This module contains the foundational classes and interfaces that power
the entire simulation ecosystem.
"""

from .entities import Freelancer, Client, Contract, Transaction
from .simulation_engine import SimulationEngine
from .scenario import Scenario
from .metrics import MetricsCollector

__all__ = [
    'Freelancer',
    'Client', 
    'Contract',
    'Transaction',
    'SimulationEngine',
    'Scenario',
    'MetricsCollector'
]