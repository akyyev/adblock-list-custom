# Supplemental DNS blocklist

Use `ios-dns-supplement.adblock` alongside FutureMind's original list. It follows
the original `category/service/domain` import format. The original file's header
is dated 2020-12-09 and contains 810 unique rules.

This supplement is derived from **HaGeZi Multi LIGHT**, retrieved November 25,
2026, with source version `2026.1125.1630.46`. Its 85,887 domains produce 171,412
supplemental rules after removing 362 identical rules from the original list.
Each source domain produces an exact rule and a `*.domain` rule, preserving
HaGeZi's intended subdomain coverage. These counts describe rules, not newly
discovered or individually confirmed live advertising servers. Only identical
rules are removed; there can still be overlapping coverage with the original's
wildcards or with the app's handling of plain domains.

Light is an extensive, size-conscious starting point. Its scope includes ads,
trackers, metrics, telemetry and some badware. It is curated upstream rather than
being a hand-picked list of unverified advertising-looking hostnames.

## Import

1. Keep your existing FutureMind list enabled.
2. In AdBlock for iOS, use **Settings → Import DNS rules**, as directed by the
   original list, and import `ios-dns-supplement.adblock` into the **0.0.0.0, ::**
   blocking group. Menu wording may differ in your installed version.
3. If the app requires a URL, host the file somewhere you control and use its
   direct raw-file URL. The local file has not been published or given a public URL.
4. Check your regularly used apps and sites after import. If something breaks,
   disable the supplement to isolate the cause, then remove the affected rule
   and its wildcard rule as needed. Edits to generated files are overwritten on rebuild.

Wildcard support is documented in the app's release notes. The output has been
checked for valid domain syntax, unique rules, exact baseline duplicates and
correct three-field serialization. Import speed, memory use and actual blocking
behavior have **not** been tested on an iPhone. Even Light becomes a substantial
file when represented as separate exact and wildcard rules.

DNS filtering cannot selectively remove ads served from the same hostname as
wanted content. This is not a promise to remove every ad, particularly in video
and social apps. Blocking a whole shared service domain can break that service.

## Refresh

The included source snapshots and `build-report.json` record the exact inputs
and their SHA-256 hashes. No background updater or scheduled task is installed.
To refresh manually, run these commands from this directory (internet required):

```sh
curl -fsSL https://raw.githubusercontent.com/FutureMind/adblock-ios-rules/master/ios-dns-rules.adblock -o sources/futuremind.adblock
curl -fsSL https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/light-onlydomains.txt -o sources/hagezi-light.txt
python3 scripts/build.py
```

Proceed with the build only if both downloads succeed. The build uses only the
saved files and requires Python 3, with no third-party packages. Reimport the
regenerated supplement to apply updates. Consult `build-report.json` for the
current counts and upstream version; the figures above describe the first build.

## Sources and license

- [FutureMind original rules](https://github.com/FutureMind/adblock-ios-rules)
- [HaGeZi DNS blocklists and Light description](https://github.com/hagezi/dns-blocklists#light)
- [HaGeZi source file](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/light-onlydomains.txt)
- [AdBlock release notes, including DNS wildcard support](https://apps.apple.com/be/app/adblock/id691121579)

The blocklists are distributed under GPL-3.0; the included `LICENSE` is the
upstream license. Preserve attribution, license and corresponding source/build
files when redistributing this modified list. Original list authors retain their
copyrights. The modification converts HaGeZi's source into FutureMind's import
format and excludes identical original rules. The build script is also provided
under GPL-3.0.
