"""
Core entity definitions for the SB 988 compliance simulator.

This module defines the primary entities in the freelancer-client ecosystem:
freelancers, clients, contracts, and transactions.
"""

from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import Dict, List, Optional, Any
from decimal import Decimal
import uuid


class FreelancerType(Enum):
    """Types of freelancers based on work characteristics."""
    INDEPENDENT_CONTRACTOR = "independent_contractor"
    GIG_WORKER = "gig_worker"
    CONSULTANT = "consultant"
    CREATIVE_PROFESSIONAL = "creative_professional"
    TECHNICAL_SPECIALIST = "technical_specialist"


class ClientType(Enum):
    """Types of clients based on organization characteristics."""
    SMALL_BUSINESS = "small_business"
    MEDIUM_ENTERPRISE = "medium_enterprise"
    LARGE_CORPORATION = "large_corporation"
    STARTUP = "startup"
    NON_PROFIT = "non_profit"
    GOVERNMENT = "government"


class ContractStatus(Enum):
    """Contract lifecycle states."""
    DRAFT = "draft"
    NEGOTIATING = "negotiating"
    ACTIVE = "active"
    COMPLETED = "completed"
    TERMINATED = "terminated"
    DISPUTED = "disputed"


class ComplianceStatus(Enum):
    """SB 988 compliance states."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"
    DISPUTED = "disputed"


@dataclass
class Freelancer:
    """Represents a freelancer in the ecosystem."""
    
    id: str
    name: str
    freelancer_type: FreelancerType
    skills: List[str]
    experience_years: float
    hourly_rate: Decimal
    location: str
    created_at: datetime
    
    # SB 988 specific attributes
    sb988_aware: bool = False
    compliance_preference: str = "neutral"  # strict, flexible, neutral
    administrative_capacity: float = 0.5  # 0-1 scale
    
    # Economic attributes
    annual_income: Optional[Decimal] = None
    primary_client_dependency: float = 0.0  # percentage of income from top client
    
    # Behavioral attributes
    risk_tolerance: float = 0.5  # 0-1 scale
    negotiation_skill: float = 0.5  # 0-1 scale
    market_knowledge: float = 0.5  # 0-1 scale
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class Client:
    """Represents a client in the ecosystem."""
    
    id: str
    name: str
    client_type: ClientType
    industry: str
    size: str  # employees count range
    location: str
    created_at: datetime
    
    # Financial attributes
    annual_revenue: Optional[Decimal] = None
    freelancer_spend_budget: Optional[Decimal] = None
    
    # SB 988 specific attributes
    sb988_awareness: float = 0.5  # 0-1 scale
    compliance_priority: str = "medium"  # high, medium, low
    legal_resources: float = 0.5  # 0-1 scale
    
    # Behavioral attributes
    risk_aversion: float = 0.5  # 0-1 scale
    negotiation_power: float = 0.5  # 0-1 scale
    market_influence: float = 0.5  # 0-1 scale
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class Contract:
    """Represents a contract between a freelancer and client."""
    
    id: str
    freelancer_id: str
    client_id: str
    title: str
    description: str
    status: ContractStatus
    created_at: datetime
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    # Financial terms
    total_value: Decimal = Decimal('0')
    payment_terms: str = "net_30"
    currency: str = "USD"
    
    # Work characteristics
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    deliverables: List[str] = None
    milestones: List[Dict[str, Any]] = None
    
    # SB 988 compliance
    sb988_compliant: ComplianceStatus = ComplianceStatus.PENDING_REVIEW
    compliance_score: float = 0.0  # 0-1 scale
    compliance_requirements: List[str] = None
    administrative_burden_score: float = 0.0  # hours of admin work
    
    # Contract terms that affect compliance
    exclusivity_clause: bool = False
    location_requirements: Optional[str] = None
    equipment_provided: bool = False
    supervision_level: str = "minimal"  # minimal, moderate, high
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if self.deliverables is None:
            self.deliverables = []
        if self.milestones is None:
            self.milestones = []
        if self.compliance_requirements is None:
            self.compliance_requirements = []


@dataclass
class Transaction:
    """Represents a financial transaction in the ecosystem."""
    
    id: str
    contract_id: str
    freelancer_id: str
    client_id: str
    amount: Decimal
    transaction_date: datetime
    payment_method: str
    status: str  # pending, completed, failed, disputed
    
    # SB 988 related costs
    compliance_costs: Decimal = Decimal('0')
    administrative_overhead: Decimal = Decimal('0')
    dispute_costs: Decimal = Decimal('0')
    
    # Metadata
    description: Optional[str] = None
    reference_number: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class MarketSnapshot:
    """Represents the state of the market at a point in time."""
    
    timestamp: datetime
    total_freelancers: int
    total_clients: int
    active_contracts: int
    total_transaction_volume: Decimal
    average_hourly_rate: Decimal
    compliance_rate: float
    
    # Economic indicators
    market_demand: float = 0.5  # 0-1 scale
    regulatory_pressure: float = 0.5  # 0-1 scale
    economic_uncertainty: float = 0.5  # 0-1 scale