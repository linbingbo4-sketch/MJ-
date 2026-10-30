# BEYOND THE SPOTLIGHT — working rules

## Where to edit
- `index.html` is generated. Edit the parts in `src/*.part` (and `src/head.html`), then run `python3 build.py`.
- Parts are concatenated in file-name order: every `<style>` into one stylesheet, every `<script>` into one script.

## Desktop and phone must show the same thing
The talk is checked on a phone as often as it is given from a laptop. Anything the desktop has, the phone has.

- Quality tiers (`src/03b-quality.part`) may only make a feature **cheaper** (lower resolution, fewer particles,
  lower frame rate, still instead of moving, plain blending instead of blend modes). They must never hide it.
  No `display: none`, no early `return`, no `Q.tier !== 'low'` / `LITE` / `TOUCH` check that removes a visible feature.
- `LITE` / `TOUCH` may change *how* something is reached (tap instead of hover, first tap loads the video player),
  not *whether* it exists. Anything clickable on the desktop is tappable on the phone.
- New effects go in for every tier at once. If a phone cannot afford the full version, give it a cheaper version
  of the same thing, in the same commit.

## Before every push
```
python3 build.py
python3 -m http.server 8000 &          # from the repo root
node tests/parity.js http://localhost:8000/index.html
```
`tests/parity.js` opens every beat on a desktop (high tier) and on an iPhone (touch, low tier) and fails if the phone
is missing any feature the desktop shows (subtitles, now-playing card, ∞ switch, MV switches and question, grain,
overlays, colour grade, particles, 3D entrances, tappable pieces, photos, figures, texts, scene animations).
It must print `✓ desktop and phone show the same features on every beat`. When you add a new kind of feature,
add it to the snapshot in `tests/parity.js` in the same commit.

## Other constraints
- Photos: freely licensed only (Wikimedia Commons, credit printed on the print). Videos and music: official YouTube
  uploads only, embedded or opened on youtube.com — never a third-party mirror or link.
- Keep the iPhone safe: WebKit sizes every composited layer by device pixel ratio. Avoid new full-stage layers that
  animate continuously on the low tier; prefer static paints there.
