# World2Vision — Seeing the Sky

An open, textbook-style field guide to building computer-vision systems that **detect and
track small, fast-moving objects in the air** — drones, aircraft, birds, balloons, and the
wider family of autonomous aerial vehicles — from a moving camera.

It starts from an empty repository and a camera pointed at nothing but clouds, and follows one
genuinely hard problem all the way to a model running on the vehicle. No background in machine
learning is assumed; every term is defined the first time it appears. The failures are left in
on purpose — they are the curriculum.

> **The pipeline is the product.** The model is the most swappable part of the whole system.
> Ten of the twelve chapters are about the machinery around it, because that is where the real
> engineering — and the real failures — live.

## Read it

The site is plain static HTML. Open `index.html` locally, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

When published with GitHub Pages (Settings → Pages → deploy from `main`, root), it is browsable
online. The `.nojekyll` file tells Pages to serve the files as-is.

## The book

**Part I — The problem & the shape**
1. Seeing Small Things in a Big Sky — why airborne detection is hard
2. The Shape of the System — the architecture the rest of the book hangs on

**Part II — Manufacturing truth**
3. Building Worlds — deterministic synthetic-data generation
4. Truth From Geometry — deriving labels from the camera math
5. Datasets That Don't Lie — immutable, leakage-guarded, license-gated data

**Part III — Learning to see**
6. The Detectors — choosing and training a model (the swappable part)
7. The Sim-to-Real Gap — the central drama, quantified and closed
8. Tiny Objects & Tiling — keeping a twenty-pixel object alive

**Part IV — Judgment & the loop**
9. Measuring What Matters — honest evaluation and failure analysis
10. Off the Desktop — export, quantization, and running on the edge
11. Closing the Loop — the system that improves itself

## How the site is built

Chapters are authored as HTML **body fragments** in `chapters/_bodies/`. A dependency-free
Python script wraps each fragment in the shared shell — sidebar table of contents, mobile
drawer, reading-progress rail, and prev/next navigation:

```bash
python3 build.py     # regenerates index.html and chapters/*.html
```

The design system (a single instrument-panel dark theme with a clean light mode) lives in
`assets/style.css`; small progressive enhancements are in `assets/site.js`.

```
w2v/
├── index.html               ← generated landing page
├── build.py                 ← the static-site builder
├── .nojekyll
├── assets/
│   ├── style.css            ← the whole design system
│   └── site.js
└── chapters/
    ├── _bodies/             ← author here (body fragments + index body)
    └── *.html               ← generated pages
```

To edit a chapter, change its fragment in `chapters/_bodies/` and re-run `python3 build.py`.

## License

Text and code are released for free reading, forking, and teaching. Verify the license of any
external model, weights, dataset, or asset you use in your own build — as Chapters 5 and 6
insist, a repository's code license tells you nothing about the rights to its weights or data.
