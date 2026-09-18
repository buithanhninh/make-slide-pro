"""
scripts/macc_council/gate3_micro_pedagogy/__init__.py
Gate 3: Micro-Pedagogy & Scientific Precision
Exports Agents 5 through 10.
"""

from .agent05_domain_pedagogy import DomainPedagogyScholar
from .agent06_mathematical_omml import MathematicalOMMLValidator
from .agent07_natural_language import NaturalLanguagePurist
from .agent08_assertion_cognitive import AssertionCognitiveArbiter
from .agent09_adversarial_critic import AdversarialContentCritic
from .agent10_master_rewriter import MasterPedagogicalRewriter

__all__ = [
    "DomainPedagogyScholar",
    "MathematicalOMMLValidator",
    "NaturalLanguagePurist",
    "AssertionCognitiveArbiter",
    "AdversarialContentCritic",
    "MasterPedagogicalRewriter"
]
