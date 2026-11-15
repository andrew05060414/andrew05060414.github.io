# Andrew Wang · 王施元

Personal website for Andrew Wang, an MS ECE student at Carnegie Mellon working on LLM infrastructure, backend systems, and reliable AI-assisted development.

**[Visit the website](https://andrew05060414.github.io/)** · **[中文版](https://andrew05060414.github.io/zh/)**

This repository is the canonical source for the website. It implements the owner's approved Console / PR-grid design as static HTML, CSS, and a small progressive enhancement script. The former design exploration is retained separately; no private repository history or raw conversation logs are included here.

## Develop

```sh
python -m venv .venv
# Activate the environment using the command appropriate to your shell.
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/verify.py
python -m http.server 8000 --directory dist
```

Edit bilingual copy and reviewed public evidence in `content/`, markup in `templates/`, and styles or interactions in `assets/`. Rebuild after editing. All reading and contact links work without JavaScript; native dialogs and a persistent light/dark theme enhance the page when JavaScript is available.

## Publish

Pull requests run the artifact checks. Merging into `main` builds and deploys to GitHub Pages. The workflow uses the built `dist/` artifact; source directories are not served as part of the website. To roll back, revert the relevant commit and let the same workflow redeploy.

## Evidence and privacy

- The PR grid is a **2026-10-28 snapshot** of classifications, not a live feed or a claim that every PR merged. The distribution is 185 auto, 221 ai-review, 203 look-after, 43 look-before, and 13 owner.
- Historical contribution counts include authorship and credited co-authorship. They describe activity, not impact or sole authorship. Selected public PRs are linked for inspection.
- PXRead, Antiochus, and Chronicle are private personal projects. Only selected descriptions appear; no private code, paths, infrastructure addresses, or raw ledger is published.
- Internship descriptions come from the owner's supplied background; they are not independent benchmark evidence.
- No phone number, analytics, advertising trackers, cookies, or résumé PDF is published. Résumé requests go to email.

Fonts are self-hosted. JetBrains Mono and VT323 are distributed under the SIL Open Font License; their notices are in `assets/`. The reference design was supplied by the site owner. See [DESIGN.md](DESIGN.md) for the visual contract and [docs/CONTENT.md](docs/CONTENT.md) for editorial boundaries.
