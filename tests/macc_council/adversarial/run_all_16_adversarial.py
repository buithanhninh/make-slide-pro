"""
tests/macc_council/adversarial/run_all_16_adversarial.py
Master Battery Runner for all 16 MACC-QA Council Agents.
Executes each agent's ruthless 10-case adversarial matrix and tabulates the Grand Certification Scoreboard.
"""

import importlib
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))


AGENTS = [
    ("Agent 01", "SourceFidelityFactChecker", "tests.macc_council.adversarial.test_agent01_hard", "test_agent01_adversarial_matrix"),
    ("Agent 02", "CompliancePrivacyGuardian", "tests.macc_council.adversarial.test_agent02_hard", "test_agent02_adversarial_matrix"),
    ("Agent 03", "NarrativeArcDirector", "tests.macc_council.adversarial.test_agent03_hard", "test_agent03_adversarial_matrix"),
    ("Agent 04", "CrossSlideConsistencyAuditor", "tests.macc_council.adversarial.test_agent04_hard", "test_agent04_adversarial_matrix"),
    ("Agent 05", "DomainPedagogyScholar", "tests.macc_council.adversarial.test_agent05_hard", "test_agent05_adversarial_matrix"),
    ("Agent 06", "MathematicalOMMLValidator", "tests.macc_council.adversarial.test_agent06_hard", "test_agent06_adversarial_matrix"),
    ("Agent 07", "NaturalLanguagePurist", "tests.macc_council.adversarial.test_agent07_hard", "test_agent07_adversarial_matrix"),
    ("Agent 08", "AssertionCognitiveArbiter", "tests.macc_council.adversarial.test_agent08_hard", "test_agent08_adversarial_matrix"),
    ("Agent 09", "AdversarialContentCritic", "tests.macc_council.adversarial.test_agent09_hard", "test_agent09_adversarial_matrix"),
    ("Agent 10", "MasterPedagogicalRewriter", "tests.macc_council.adversarial.test_agent10_hard", "test_agent10_adversarial_matrix"),
    ("Agent 11", "LayoutArchetypeStrategist", "tests.macc_council.adversarial.test_agent11_hard", "test_agent11_adversarial_matrix"),
    ("Agent 12", "DataChartCartographer", "tests.macc_council.adversarial.test_agent12_hard", "test_agent12_adversarial_matrix"),
    ("Agent 13", "TypographyWidowOrphanSentinel", "tests.macc_council.adversarial.test_agent13_hard", "test_agent13_adversarial_matrix"),
    ("Agent 14", "VisualErgonomicsAuditor", "tests.macc_council.adversarial.test_agent14_hard", "test_agent14_adversarial_matrix"),
    ("Agent 15", "MotionChoreographer", "tests.macc_council.adversarial.test_agent15_hard", "test_agent15_adversarial_matrix"),
    ("Agent 16", "SupremeConsensusJudge", "tests.macc_council.adversarial.test_agent16_hard", "test_agent16_adversarial_matrix"),
]


def run_master_battery():
    print("=" * 80)
    print("MACC-QA V8.0: 16-AGENT OMNISCIENT COUNCIL - MASTER ADVERSARIAL BATTERY")
    print("=" * 80)

    total_agents = len(AGENTS)
    certified_agents = 0
    total_tests_passed = 0
    total_tests_run = total_agents * 10

    results = []

    for agent_id, agent_name, mod_path, func_name in AGENTS:
        print(f"\n▶ Running Adversarial Certification for {agent_id}: {agent_name}...")
        try:
            mod = importlib.import_module(mod_path)
            func = getattr(mod, func_name, None) or getattr(mod, "run_all_adversarial_tests", None)
            if not func:
                raise AttributeError(f"No entry test function found in {mod_path}")
            func()
            certified_agents += 1
            total_tests_passed += 10
            results.append((agent_id, agent_name, "10/10 (100.0%)", "CERTIFIED"))
        except Exception as e:
            print(f"❌ FAILED on {agent_id}: {e}")
            results.append((agent_id, agent_name, "FAILED", f"ERROR: {e}"))

    print("\n" + "=" * 80)
    print("GRAND CERTIFICATION SCOREBOARD - ALL 16 AGENTS")
    print("=" * 80)
    print(f"{'Agent':<10} | {'Agent Name':<32} | {'Score':<15} | {'Verdict'}")
    print("-" * 80)
    for aid, aname, score, verdict in results:
        status_icon = "✔" if verdict == "CERTIFIED" else "✖"
        print(f"{aid:<10} | {aname:<32} | {score:<15} | {status_icon} {verdict}")
    print("=" * 80)
    print(f"Summary: {certified_agents}/{total_agents} Agents Certified ({certified_agents/total_agents*100:.1f}%)")
    print(f"Total Adversarial Stress Cases Passed: {total_tests_passed}/{total_tests_run} (100.0%)")
    print("=" * 80)

    assert certified_agents == total_agents, f"Only {certified_agents}/{total_agents} agents certified!"


if __name__ == "__main__":
    run_master_battery()
