# Figure patterns

Read this in Phase 4, while drawing. These are the shapes a topic book needs, with copy-ready
SVG. They use the classes defined in `assets/book-shell.html`: `fig-stroke`, `fig-stroke-thin`,
`fig-dash`, `fig-text`, `fig-text-sm`.

## Two rules specific to an interview book

**Every figure must be redrawable on a whiteboard in about sixty seconds.** The reader is not
going to admire your diagram; they are going to reproduce it in front of a stranger. Which means:
few boxes, no gradients, no decoration, and the labels short enough to say out loud while drawing.
If a figure cannot be redrawn from memory, it has failed at its actual job even if it is correct.

**Put the insight in the layout.** If the chapter's point is that the cache sits after
authorization and therefore cannot serve unauthorized requests, draw it after authorization. A
figure that merely restates the prose is decoration; a figure whose geometry carries the argument
is why books have figures at all.

## Why hand-authored SVG rather than Mermaid

Mermaid lays out for you, which sounds like a saving and is not: you lose the ability to place a
box where the argument needs it, and placement is where the meaning lives. Hand-authored SVG also
renders identically everywhere, needs no library, and is a few dozen lines.

## Conventions that keep figures consistent

Consistency across chapters is what makes a set of figures feel like one book. Hold these fixed:

- **viewBox** `0 0 600 H` on a wide page, `0 0 460 H` on a normal one. Pick H so the drawing fills
  it without slack, usually 150 to 300.
- **Boxes** 1.25 stroke for primary nodes, `fig-stroke-thin` for secondary, and
  `style="stroke-width:2"` for the single most important node. One emphasized box per figure;
  two emphasize nothing.
- **Text baselines** about 6px below a box's vertical centre. For a 40-tall box at `y=50`, labels
  go at `y=75`. Two-line labels at centre−4 and centre+9.
- **Text inset** 14 to 16px from the box's left edge.
- **Arrows** are a line plus a three-segment head, always two elements:
  ```html
  <path d="M130 70 L180 70" class="fig-stroke" />
  <path d="M174 66 L180 70 L174 74" class="fig-stroke" />
  ```
- **Dashed** (`fig-dash`) means "not the main path": an exception route, a boundary, a return edge.
- **A footline**: a thin rule with one small-text sentence under it, stating the figure's own
  takeaway. Use it whenever the conclusion is the reason the figure exists.

Every `<svg>` needs `role="img"` and an `aria-label` that describes the nodes, the direction of
flow, and the conclusion — written for someone who cannot see it, not as a title.

## Pattern: linear pipeline

Request paths, processing stages, encode/decode round trips.

```html
<svg viewBox="0 0 600 150" role="img" aria-label="A request passes through three stages; the third is emphasized because it is where the latency is spent.">
  <rect x="20" y="50" width="110" height="40" class="fig-stroke" />
  <text x="36" y="75" class="fig-text">request</text>
  <path d="M130 70 L180 70" class="fig-stroke" /><path d="M174 66 L180 70 L174 74" class="fig-stroke" />
  <rect x="180" y="50" width="110" height="40" class="fig-stroke" />
  <text x="196" y="75" class="fig-text">stage</text>
  <path d="M290 70 L340 70" class="fig-stroke" /><path d="M334 66 L340 70 L334 74" class="fig-stroke" />
  <rect x="340" y="50" width="110" height="40" class="fig-stroke" style="stroke-width:2" />
  <text x="356" y="75" class="fig-text">the cost</text>
  <line x1="20" y1="120" x2="580" y2="120" class="fig-stroke-thin" />
  <text x="20" y="138" class="fig-text-sm">the takeaway, stated inside the drawing</text>
</svg>
```

## Pattern: the trade-off axis

The single most useful figure in an interview book, because trade-off questions are the most
common senior filter. Two axes, four named regions, and your subject's options placed as points.
The reader learns not only where each option sits but what the empty corner means.

```html
<svg viewBox="0 0 600 260" role="img" aria-label="A two-axis plot of cost against latency with four options placed; the cheap and fast corner is empty, which is the point of the figure.">
  <line x1="70" y1="210" x2="560" y2="210" class="fig-stroke" />
  <line x1="70" y1="210" x2="70" y2="30" class="fig-stroke" />
  <text x="480" y="228" class="fig-text-sm">cost per call &rarr;</text>
  <text x="18" y="40" class="fig-text-sm">tail</text>
  <text x="18" y="52" class="fig-text-sm">latency</text>
  <circle cx="170" cy="80" r="4" class="fig-stroke" style="fill:var(--fg)" />
  <text x="182" y="84" class="fig-text-sm">option A: cheap, slow</text>
  <circle cx="430" cy="170" r="4" class="fig-stroke" style="fill:var(--fg)" />
  <text x="442" y="174" class="fig-text-sm">option B</text>
  <path d="M120 150 L520 60" class="fig-dash" />
  <text x="300" y="120" class="fig-text-sm">the frontier: everything below is unavailable</text>
</svg>
```

Name the empty corner in the caption. "Nothing sits bottom-left, and the interview question is
always why" is a sentence a reader will reuse verbatim.

## Pattern: layered stack

For anything with levels of abstraction: the network stack, a storage hierarchy, a serving stack.
Stack rectangles with a shared left edge, and annotate to the right what crosses each boundary.
The boundary annotations are the content; the boxes are scaffolding.

```html
<rect x="120" y="30" width="240" height="34" class="fig-stroke" />
<text x="134" y="52" class="fig-text">your code</text>
<rect x="120" y="64" width="240" height="34" class="fig-stroke-thin" />
<text x="134" y="86" class="fig-text-sm">the library</text>
<text x="376" y="60" class="fig-text-sm">what crosses here, and what it costs</text>
<path d="M366 52 L372 52" class="fig-stroke-thin" />
```

## Pattern: feedback loop

Retry logic, control loops, autoscaling, agent loops: anything whose output re-enters as input.
Routing the return edge above the row is what makes it read as a loop rather than a branch.

```html
<path d="M460 70 L460 30 L189 30 L189 62" class="fig-stroke" />
<path d="M185 56 L189 62 L193 56" class="fig-stroke" />
<text x="268" y="24" class="fig-text-sm">observe, then adjust</text>
```

## Pattern: decision diamond

Branch points, and especially gates. Draw the happy path rightward and the unhappy path downward,
so "rejected" reads as a detour. Label both edges; an unlabelled branch is a figure the reader
cannot narrate.

```html
<path d="M232 74 L296 107 L232 140 L168 107 Z" class="fig-stroke" />
<text x="198" y="103" class="fig-text-sm">under</text>
<text x="200" y="116" class="fig-text-sm">budget?</text>
<path d="M296 107 L336 107" class="fig-stroke" /><path d="M330 103 L336 107 L330 111" class="fig-stroke" />
<text x="300" y="99" class="fig-text-sm">yes</text>
<path d="M232 140 L232 186 L330 186" class="fig-stroke" /><path d="M324 182 L330 186 L324 190" class="fig-stroke" />
<text x="238" y="164" class="fig-text-sm">shed load</text>
```

## Pattern: timeline with lanes

For sequences where *who* is doing something matters as much as when: a request across services,
a handshake, a failover. One horizontal lane per actor, a label at the left, and time running
right. Put the moment the chapter is about on its own vertical dashed line and label it above.

```html
<text x="14" y="46" class="fig-text-sm">client</text>
<line x1="80" y1="40" x2="580" y2="40" class="fig-stroke-thin" />
<text x="14" y="106" class="fig-text-sm">server</text>
<line x1="80" y1="100" x2="580" y2="100" class="fig-stroke-thin" />
<path d="M120 40 L240 100" class="fig-stroke" /><path d="M234 92 L240 100 L230 99" class="fig-stroke" />
<line x1="330" y1="20" x2="330" y2="130" class="fig-dash" />
<text x="336" y="26" class="fig-text-sm">the timeout fires here</text>
```

## Pattern: state machine

Retry states, connection states, lifecycle. Circles or rounded rects, edges labelled with the
event that causes the transition, and the terminal state emphasized. Keep it to five states; a
six-state diagram on a book page is unreadable and unmemorable.

## Pattern: before and after

For the argument that some change collapses complexity. Two states side by side on one wide
viewBox, split by a vertical dashed rule, an all-caps small label over each half. Draw the tangled
version with `fig-stroke-thin` so it reads as noise and the clean one with `fig-stroke` so it
reads as signal. Six crossing lines beside three straight ones is an argument prose cannot make
as fast.

```html
<text x="10" y="16" class="fig-text-sm">BEFORE: a client per backend</text>
<line x1="310" y1="20" x2="310" y2="200" class="fig-dash" />
<text x="330" y="16" class="fig-text-sm">AFTER: one interface</text>
```

## Pattern: the numbers figure

Where a chapter's point is arithmetic — capacity, cost, a latency budget — draw the budget rather
than tabulating it. A single horizontal bar segmented by where the milliseconds go, with each
segment labelled and the total at the right, is the figure a reader will redraw when asked to
"walk me through where the time goes".

```html
<rect x="20" y="60" width="180" height="30" class="fig-stroke" />
<text x="30" y="80" class="fig-text-sm">network 40ms</text>
<rect x="200" y="60" width="90" height="30" class="fig-stroke-thin" />
<text x="210" y="80" class="fig-text-sm">queue 20ms</text>
<rect x="290" y="60" width="240" height="30" class="fig-stroke" style="stroke-width:2" />
<text x="300" y="80" class="fig-text-sm">inference 120ms &mdash; the whole budget lives here</text>
<text x="536" y="80" class="fig-text-sm">180ms</text>
```

## Sizing and legibility

Figures cap at `max-height: 54vh`, so a tall drawing shrinks its own text below readability. If a
figure needs more than about 300 units of height, it is two figures on two pages. Pagination is
free; cramped figures are not.

The validator warns about a missing `viewBox` or `aria-label`, but only a rendered screenshot
shows you a label that has drifted outside its box. Shoot the figure pages before publishing.
