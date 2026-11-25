#!/usr/bin/env python3
"""Convert Peter Lowe's domain filters into a small FutureMind supplement."""
import hashlib
import json
from build import ROOT, entries, valid_domain

source = ROOT / 'sources/peter-lowe.txt'
text = source.read_text()
domains = set()
for line in text.splitlines():
    line = line.strip()
    if not line or line.startswith(('!', '[')):
        continue
    if not (line.startswith('||') and line.endswith('^')
            and valid_domain(line[2:-1])):
        raise ValueError(f'Unsupported source rule: {line}')
    domains.add(line[2:-1])
if len(domains) < 1000:
    raise ValueError('Suspiciously small source; refusing to build')
baseline = {line.rsplit('/', 1)[-1].lower()
            for line in entries((ROOT / 'sources/futuremind.adblock').read_text())}
candidates = {rule for domain in domains for rule in (domain, '*.' + domain)}
rules = sorted(candidates - baseline)
header = (
    '# Minimal supplemental DNS rules for FutureMind AdBlock for iOS\n'
    '# Source: Peter Lowe, https://pgl.yoyo.org/adservers/\n'
    '# Converted by scripts/build_minimal.py; source preserved in sources/peter-lowe.txt\n'
    '# Use alongside the original FutureMind list, instead of the HaGeZi supplement\n'
    '# Import into the 0.0.0.0, :: blocking group\n'
    f'# Rules: {len(rules)}\n'
)
output = header + ''.join(f'Supplement/Peter Lowe/{rule}\n' for rule in rules)
parsed = [line.split('/') for line in entries(output)]
assert all(len(parts) == 3 for parts in parsed)
assert len(parsed) == len(set(parts[-1] for parts in parsed))
assert {parts[-1] for parts in parsed} == candidates - baseline
(ROOT / 'ios-dns-minimal.adblock').write_text(output)
report = {
    'source': 'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'source_date': next(line for line in text.splitlines() if line.startswith('!Last modified:')),
    'source_domains': len(domains),
    'identical_baseline_rules_removed': len(candidates & baseline),
    'supplement_rules': len(rules),
    'bytes': len(output.encode()),
}
(ROOT / 'minimal-build-report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
