# Hosted mathematics checks

The read-only [workflow](../../.github/workflows/hosted-math.yml) compares each mathematical expression in every tracked Markdown page with its rendering on the actual commit-pinned GitHub page. It captures both 1440-pixel and 760-pixel viewports, saves screenshots and accessible mathematics, and reports missing hosts, changed mathematical structure, renderer errors and display geometry failures. The job has only `contents: read`, does not persist checkout credentials, and uses no secrets or certificate-trust changes.

To reproduce with Node.js 18+, Python 3.10+, Git and a default-trust Chromium environment:

```bash
npm install --prefix /tmp/symmetry-hosted-deps playwright@1.56.1 mathjax-full@3.2.1
/tmp/symmetry-hosted-deps/node_modules/.bin/playwright install chromium
NODE_PATH=/tmp/symmetry-hosted-deps/node_modules node verification/hosted/capture_hosted_math.cjs \
  --root "$PWD" --repository GoGoKo699/Low-Rank-Quantum-Symmetry \
  --revision "$(git rev-parse HEAD)" --contract verification/hosted/math-contract.json \
  --output /tmp/symmetry-hosted-evidence
```

Use a new output directory for each run. Dependencies and browser installation belong outside the source tree. Public pages must be available at the supplied full commit SHA. The bundled collector and comparison helper are preserved together from the 2026-11-01 verified tool revision; their source hashes are recorded with the review evidence.

The workflow artifact contains `hosted-report.json`, expression inventories, captured MathML, comparison results, HTML and screenshots. The [headline contract](math-contract.json) additionally pins the expected accessible text of the main resource bounds and exact symmetry promise. A passing automated report supports source-to-render agreement on that revision. It does not establish proof validity or replace visual inspection of equations, tables and navigation. Artifacts expire after 14 days; a durable review should retain the report and consequential observations separately.
