# benchmark script
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json, time
from typing import Dict, Any, List
from scripts.macc_council.orchestrator import MultiRoundCouncilOrchestrator
from scripts.macc_council.models import Severity

def extract_canonical_text(canonical_path: Path) -> str:
    with open(canonical_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    text_parts = []
    for sec in data.get('sections', []):
        text_parts.append(sec.get('title', ''))
        text_parts.extend(sec.get('paragraphs', []))
        for atom in sec.get('atoms', []):
            text_parts.append(atom.get('verbatim', ''))
    return '\n'.join(text_parts)

def run_benchmark():
    base_dir = Path('Du_An_Outputs/Bai_1__Nhap_mon_DSH')
    blueprints_path = base_dir / 'slide-blueprints.json'
    canonical_path = base_dir / 'canonical-content.json'
    v73_report_path = base_dir / 'qa-certification-report.json'

    print('=' * 70)
    print('MACC-QA V8.0 EMPIRICAL BENCHMARK: BAI 1 (NHAP MON DSH)')
    print('=' * 70)

    with open(blueprints_path, 'r', encoding='utf-8') as f:
        deck_target = json.load(f)
    with open(v73_report_path, 'r', encoding='utf-8') as f:
        v73_report = json.load(f)

    canonical_text = extract_canonical_text(canonical_path)
    context = {
        'canonical_text': canonical_text,
        'source_text': canonical_text,
        'deck_title': deck_target.get('deck_title', 'Bai 1: Nhap mon DSH')
    }

    slides_list = deck_target.get("slides", [])
    print(f"Loaded deck with {len(slides_list)} slides.")
    print(f"Extracted canonical text: {len(canonical_text)} characters.")
    print(f"Old v7.3 Certification Score: {v73_report.get('combined_score')}% ({v73_report.get('certification_status')})")
    print("-" * 70)

    orchestrator = MultiRoundCouncilOrchestrator()
    print('Running MACC-QA V8.0 Council Round 1 Audit (As-Is Baseline)...')
    t0 = time.time()
    r1_report, _ = orchestrator.run_round(deck_target, context=context, auto_remediate=False)
    t_r1 = time.time() - t0

    r1_findings = []
    for g_name, g_rep in r1_report.gate_reports.items():
        r1_findings.extend(g_rep.findings)

    p0_count = sum(1 for f in r1_findings if f.severity == Severity.P0)
    p1_count = sum(1 for f in r1_findings if f.severity == Severity.P1)
    p2_count = sum(1 for f in r1_findings if f.severity == Severity.P2)

    findings_by_agent = {}
    for f in r1_findings:
        findings_by_agent.setdefault(f.agent, []).append(f)

    print(f'Round 1 Audit completed in {t_r1:.3f}s')
    print(f'Round 1 Final Score: {r1_report.final_score:.2f}/100.0')
    print(f'Total Defects Uncovered: {len(r1_findings)} (P0: {p0_count}, P1: {p1_count}, P2: {p2_count})')
    print(f'Council Certified: {r1_report.certified}')
    print('\nDefects breakdown by Agent:')
    for ag_name, ag_f in sorted(findings_by_agent.items()):
        print(f'  - [{ag_name}]: {len(ag_f)} issues')
        for issue_item in ag_f[:3]:
            print(f'      * ({issue_item.severity.value}) Slide {issue_item.slide_id}: {issue_item.issue[:90]}')

    print('-' * 70)
    print('Running MACC-QA V8.0 Multi-Round Dialectical Convergence Loop (Max 5 Rounds)...')
    def on_round(r_idx, rep):
        print(f'  [Round {r_idx}] Score: {rep.final_score:.2f}, Certified: {rep.certified}')

    t1 = time.time()
    converged_report = orchestrator.run_convergence_loop(
        deck_target,
        context=context,
        max_rounds=5,
        on_round_callback=on_round
    )
    t_loop = time.time() - t1

    final_findings = []
    for g_name, g_rep in converged_report.gate_reports.items():
        final_findings.extend(g_rep.findings)

    print(f'\nConvergence completed in {t_loop:.3f}s across {converged_report.total_rounds} rounds.')
    cert_status_str = "CERTIFIED" if converged_report.certified else "REJECTED"
    print(f"Final Certification Status: {cert_status_str}")
    print(f"Residual Defects: {len(final_findings)}")

    summary = {
        'v73_legacy': {
            'score': v73_report.get('combined_score'),
            'status': v73_report.get('certification_status'),
            'total_findings': 1
        },
        'v80_round1': {
            'score': r1_report.final_score,
            'certified': r1_report.certified,
            'total_defects': len(r1_findings),
            'p0': p0_count, 'p1': p1_count, 'p2': p2_count,
            'defects_by_agent': {k: len(v) for k, v in findings_by_agent.items()}
        },
        'v80_converged': {
            'score': converged_report.final_score,
            'certified': converged_report.certified,
            'total_rounds': converged_report.total_rounds,
            'residual_defects': len(final_findings),
            'execution_time': t_loop
        }
    }
    with open(base_dir / 'macc_v8_benchmark_summary.json', 'w', encoding='utf-8') as out_f:
        json.dump(summary, out_f, indent=2, ensure_ascii=False)
    print('Summary saved to macc_v8_benchmark_summary.json')

if __name__ == '__main__':
    run_benchmark()
