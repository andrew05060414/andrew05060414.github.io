# Design system

Created: 2026-11-15 · Updated: 2026-11-15 · Version: 1.0

The owner's Console / PR-grid reference is the visual authority: a personal personnel file, a pixel-drawn name, a dark phosphor terminal, and a real historical PR-classification grid. This is an implementation of that direction, not a new branding exploration.

The main palette uses background `#0a0b09`, panel `#10130e`, foreground `#e6e9dd`, muted ink `#9aa292`, green `#7ee08f`, and amber `#f0b44c`. The alternate paper palette preserves the reference's warm paper and dark ink. Green and amber describe historical delivery-policy categories rather than arbitrary project status.

JetBrains Mono carries interface and body copy; VT323 carries display numerals and file titles. Chinese uses the local CJK font stack. Fonts are self-hosted, and the large name is a grid of geometric pixels from the reference's letter patterns.

Desktop pairs the name and personal statement with the PR grid. Compact layouts stack them, followed by the five file-entry links. The final entry is Contact, with a direct email route. Native dialogs present the files when scripting is available; ordinary semantic sections and anchor links remain the fallback.

Preserve visible focus, keyboard dismissal, language-specific URLs, snapshot dates, and the built/dependency distinction. Respect reduced-motion preferences and check both palettes, both languages, and a 375px viewport before shipping interface changes.

The first viewport features PXRead, Antiochus, and Chronicle directly. Their case studies use problem, engineering, and evidence sections; historical PR classifications are supporting material. Desktop layout uses actual content height rather than subtracting an estimated chrome height. Short desktop windows compact the PR-panel spacing; small screens and enlarged text retain natural page scrolling. In paper mode, inactive name pixels and the surface texture are transparent so only the letter strokes carry ink.
