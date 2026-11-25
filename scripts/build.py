#!/usr/bin/env python3
"""Build a FutureMind-compatible supplement from saved, attributed sources."""
import hashlib
import ipaddress
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URLS = {
    "futuremind.adblock": "https://raw.githubusercontent.com/FutureMind/adblock-ios-rules/master/ios-dns-rules.adblock",
    "hagezi-light.txt": "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/light-onlydomains.txt",
}


def entries(text):
    return [line.strip() for line in text.splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def valid_domain(domain):
    if len(domain) > 253 or "." not in domain:
        return False
    try:
        ipaddress.ip_address(domain)
        return False
    except ValueError:
        return all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
                   for label in domain.split("."))


def build():
    texts = {name: (ROOT / "sources" / name).read_text() for name in URLS}
    baseline = {line.rsplit("/", 1)[-1].lower()
                for line in entries(texts["futuremind.adblock"])}
    raw = entries(texts["hagezi-light.txt"])
    domains = sorted(set(raw))
    if not baseline or len(domains) < 1000:
        raise ValueError("Empty or suspiciously small source; refusing to build")
    invalid = [domain for domain in domains if not valid_domain(domain)]
    if invalid:
        raise ValueError(f"Invalid source domains: {invalid[:10]}")
    # Preserve the source's domain-and-subdomain coverage. Remove identical
    # baseline rules only: do not assume a plain baseline domain covers children.
    candidates = {rule for domain in domains for rule in (domain, '*.' + domain)}
    rules = sorted(candidates - baseline)
    header = (
        "# Supplemental DNS rules for AdBlock for iOS by Future Mind\n"
        "# Derived from HaGeZi Multi LIGHT; modified by scripts/build.py\n"
        "# License: GPL-3.0; see LICENSE and README.md\n"
        "# Import alongside the original list into the 0.0.0.0, :: group\n"
        "# Includes ads, trackers, telemetry and some badware\n"
        f"# Rules: {len(rules)}\n"
    )
    output = header + ''.join(f"Supplement/HaGeZi Light/{rule}\n" for rule in rules)
    # Verify the serialized import data, not just the input collection.
    parsed = [line.split('/') for line in entries(output)]
    assert all(len(parts) == 3 for parts in parsed)
    assert {parts[-1] for parts in parsed} == candidates - baseline
    assert len(parsed) == len(set(parts[-1] for parts in parsed))
    (ROOT / 'ios-dns-supplement.adblock').write_text(output)
    report = {
        "baseline_unique_rules": len(baseline),
        "source_unique_domains": len(domains),
        "identical_baseline_rules_removed": len(candidates & baseline),
        "supplement_rules": len(rules),
        "source_headers": [line for line in texts['hagezi-light.txt'].splitlines()
                           if line.startswith(('# Last modified:', '# Version:'))],
        "sources": {name: {"url": url, "sha256": hashlib.sha256(
            (ROOT / 'sources' / name).read_bytes()).hexdigest()} for name, url in URLS.items()},
    }
    (ROOT / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    build()
