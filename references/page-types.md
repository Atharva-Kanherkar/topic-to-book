# Page types and the assembly workflow

Read this in Phase 4, when you start writing pages. `assets/book-shell.html` carries a rendered
example of every component; this file is the copy-from reference and the rules about how much
goes on a page.

## Write in fragments, assemble at the end

A 150-page book written into one file becomes unmanageable around page thirty, and every insertion
invalidates the contents page. So write chapters as separate fragment files and let the assembler
concatenate them and number the contents:

```
chapters/
  00-cover.html          cover + how-to-use
  01-contents.html       holds <div class="toc" data-auto="true"></div>
  10-part-1.html         part title page
  11-ch1.html            chapter one: theory pages
  12-ch1-sheet.html      chapter one: practice sheet
  20-part-2.html
  ...
  90-exam.html
  91-key.html
  92-readiness.html
  99-sources.html
```

Files are concatenated in filename order, so leave gaps in the numbering: inserting a chapter
later should not mean renaming eight files.

```bash
python3 scripts/assemble_book.py chapters/ -o book.html --title "The Title" --book-id topic-slug
python3 scripts/validate_book.py book.html
```

A fragment is a bare sequence of `<section class="page">` blocks. No `<html>`, no `<style>`, no
script: the shell owns all of that.

### The attributes the machinery reads

| Attribute | On | Effect |
| --- | --- | --- |
| `data-part="Part II · Mechanisms"` | a part title page | starts a contents group |
| `data-toc="Routing policies"` | any page | a contents entry, with the page number counted at assembly |
| `data-toc-n="04"` | a page with `data-toc` | the label in the left column; omit for unnumbered entries |
| `data-ch="Four · Routing policies"` | every page of a chapter | groups quizzes and drills on the readiness page |
| `id="p-routing"` | any page | assigned automatically when `data-toc` is present, but set it yourself if you link to it |

A page can carry `data-part` and `data-toc` at once, which is how the appendices get their own
contents group without spending a page on a part title.

`data-ch` is not optional in practice: it is what lets the readiness page tell the reader which
chapter to go back to. Put the same string on the chapter's theory pages and its practice sheet.

## How much fits on a page

- **Prose page**: 350 to 450 words, or 250 with a small figure. The measure is 60 characters; a
  page that runs past the fold has already lost the format's advantage.
- **Wide page** (`class="page w"`): use for figures, tables, transcripts. 78 characters.
- **Practice sheet**: four to six graded questions, *or* two to four questions plus two open
  drills. Never more; an overfull sheet page pushes the grade button off screen.
- **Figure page**: one figure. Two figures on a page means neither is legible.

Size a page to fit **ungraded**. A graded practice sheet grows when the explanations appear, and
letting that state scroll within the page is fine — it is read after the reader has committed to
an answer. What must never scroll is the unanswered page, because a reader who cannot see the
grade button assumes there is not one.

If a page overflows, split it. The validator warns past 4,500 characters of visible text.

## Front matter

```html
<section class="page cover">
  <div class="leaf">
    <p class="cover-mark">Topic · interview preparation</p>
    <h1>The title,<br />in two lines</h1>
    <p class="sub">What the reader will be able to say, draw, and defend at the end.</p>
    <div class="imprint">
      Prepared for &nbsp; senior infrastructure interviews<br />
      Researched &nbsp; March 2026 · 140 pages · 86 questions
    </div>
  </div>
</section>
```

The contents fragment carries the auto slot, and nothing else it does not need:

```html
<section class="page">
  <div class="rh"><span>Contents</span><span>12 chapters</span></div>
  <div class="leaf"><div class="toc tight" data-auto="true"></div></div>
</section>
```

`toc tight` sets two columns and a smaller size: use it past about 25 entries, and split the
contents across two pages past about 60.

A **how to use this book** page earns its place in any book over 60 pages: the study routes by
time available, the mechanics, and what the reader should do rather than read.

## Part title

```html
<section class="page part" data-part="Part II · The mechanisms">
  <div class="leaf">
    <div class="rule-long"></div>
    <p class="part-num">Part two</p>
    <h2 class="part-title">The mechanisms</h2>
    <p class="part-gloss">One sentence on what this part establishes and why it comes here.</p>
  </div>
</section>
```

## Theory page

```html
<section class="page" data-ch="Four · Routing policies" data-toc="Routing policies" data-toc-n="04">
  <div class="rh"><span>Four · Routing policies</span><span>Cost-aware routing</span></div>
  <div class="leaf">
    <h2 class="ch-title"><span class="cn">Chapter four</span>Routing policies</h2>
    <p class="lede">The chapter's claim, in one sentence.</p>
    <h3 class="sub">A subsection</h3>
    <p>Prose. Define each term the first time it appears.</p>
    <div class="box trap">
      <span class="lab">Trap</span>
      <p>The misconception, named as a belief the reader may hold, then corrected.</p>
    </div>
    <div class="box say">
      <span class="lab">Say this</span>
      <p>The sentence worth having by heart, phrased for speech rather than for print.</p>
    </div>
  </div>
</section>
```

`.box.trap` for a misconception, `.box.say` for a line to say out loud, plain `.box` for anything
else. Use `<p class="cap"><b>Label</b> …</p>` under figures, code, and tables for the takeaway.

Code blocks are `<pre class="code"><code>…</code></pre>` with comments in `<span class="c">`. Copy
buttons are added automatically.

## Numbers page

A table with `class="num"` on the numeric cells keeps the digits in tabular figures, which is what
makes a column of latencies comparable at a glance:

```html
<div class="tw"><table>
  <thead><tr><th>Quantity</th><th class="num">Value</th><th>Source</th></tr></thead>
  <tbody>
    <tr><td>Round trip, same region</td><td class="num">0.5 ms</td><td>vendor docs, 2025</td></tr>
  </tbody>
</table></div>
```

Every number carries a unit and a source. Follow the page with a drill that asks for three of
them from memory.

## Practice sheet

One after every chapter. Graded questions first, then the open drills.

```html
<section class="page" data-ch="Four · Routing policies" data-toc="Practice sheet four">
  <div class="rh"><span>Practice sheet four</span><span>Chapter four</span></div>
  <div class="leaf">
    <h2 class="ch-title"><span class="cn">Practice sheet four</span>Routing policies</h2>
    <form class="quiz">
      <ol class="qs">
        <li class="q" data-answer="b">
          <p class="qt">The question?<span class="verdict"></span></p>
          <label><input type="radio" name="s4q1" value="a" /><span>Tempting wrong answer</span></label>
          <label><input type="radio" name="s4q1" value="b" /><span>Right answer</span></label>
          <label><input type="radio" name="s4q1" value="c" /><span>Another tempting one</span></label>
          <div class="why"><strong>b.</strong> Why b, and why a and c are tempting.</div>
        </li>
      </ol>
      <div class="quiz-bar">
        <button type="button" class="qbtn" data-action="check">Grade</button>
        <button type="button" class="qbtn" data-action="reset">Clear</button>
        <span class="score"></span>
      </div>
    </form>
    <div class="drill" style="margin-top:1.3rem">
      <span class="lab">Out loud, from memory</span>
      <div class="fr" data-id="s4-fr1">
        <p class="prompt"><span class="tag">60 sec</span><span>The prompt, as an interviewer
          would phrase it.</span></p>
        <details><summary>Model answer</summary>
          <div class="answer"><p>What a strong answer contains, in the order it says it.</p>
          <p><em>Marked down for:</em> the omission that costs the point.</p></div></details>
        <div class="rate"><span class="lab">Rate yourself</span>
          <button type="button" class="rbtn" data-rate="miss">missed</button>
          <button type="button" class="rbtn" data-rate="shaky">shaky</button>
          <button type="button" class="rbtn" data-rate="solid">solid</button>
        </div>
      </div>
    </div>
  </div>
</section>
```

Rules that matter:

- **`name` must be unique across the whole book.** Two questions sharing a radio name will
  unset each other. The validator fails on this. Use the sheet number as a prefix.
- **`data-id` on every `.fr`, unique across the book**, or the rating cannot be saved.
- **Every distractor must be a belief a reader might actually hold.** One plausible option plus
  two silly ones tests reading, not understanding.
- **The `.why` explains the distractor**, not just the answer. That is the teaching moment; the
  score is only what makes the reader read it.

## Follow-up ladder

The component that separates this from a textbook: the shape of the conversation.

```html
<div class="ladder">
  <div class="step">
    <p class="ask"><b>They open with</b>The question, verbatim as reported.</p>
    <dl>
      <dt>weak</dt><dd>The answer that recites a definition.</dd>
      <dt>solid</dt><dd>Names the trade-off and picks a side.</dd>
      <dt>strong</dt><dd class="strong">Picks a side and states what would change its mind.</dd>
    </dl>
  </div>
</div>
```

Three to four rungs per ladder, two ladders per page at most.

## Annotated mock round

```html
<div class="timer" data-min="45">
  <button type="button" class="qbtn" data-timer="start">Start</button>
  <button type="button" class="qbtn" data-timer="reset">Reset</button>
  <span class="clock">45:00</span>
  <span class="what">close the book and talk for the clock</span>
</div>
<div class="dlg">
  <div class="turn"><span class="who">them</span><div>
    <p class="said">The prompt, including the part left deliberately vague.</p></div></div>
  <div class="turn you"><span class="who">you</span><div>
    <p class="said">The answer, in the words a candidate would use.</p>
    <p class="note"><b>why</b> What this move buys, or where candidates stall here.</p></div></div>
</div>
```

Annotate the *moves*, not the content. "Narrate while you draw; a silent whiteboard reads as a
stall" is worth more than another paragraph of theory.

## Level signals

A wide table, dimensions down the left, levels across the top. Say in the caption where the
calibration came from, and mark it as inference if that is what it is.

## Flashcards

```html
<ol class="deck">
  <li class="card" data-id="c-p99">
    <button type="button" class="face">p99 versus p50, and why interviewers ask for p99</button>
    <div class="back">The answer, one or two sentences.</div>
    <div class="mark"><button type="button" class="rbtn" data-known="1">knew it</button></div>
  </li>
</ol>
<div class="deck-bar">
  <button type="button" class="qbtn" data-deck="flip">Turn all</button>
  <button type="button" class="qbtn" data-deck="clear">Unmark all</button>
  <span class="score" data-deck-score></span>
</div>
```

Six to nine cards per page. Fronts are terms, numbers, or one-line prompts; backs are one or two
sentences, never a paragraph.

## Examination, key, readiness, sources

The final examination is the same quiz markup, four to six questions per page, drawn from across
the book and weighted toward the traps. Then:

```html
<div class="key" id="answer-key"></div>          <!-- generated from every question in the book -->
<div class="meter" id="readiness"></div>         <!-- generated from saved grades and ratings -->
<button type="button" class="qbtn" id="progress-reset">Clear all progress</button>
```

The sources page is not optional. Say where the theory came from, where the interview
intelligence came from and how many accounts each claim rests on, what is inference, and which
month the research was done in.

## Cheat sheet

The last content page before the appendices: one wide page, two columns, everything worth
rereading in the ten minutes before the call. The openings, the numbers, the three sentences to
have by heart, the two questions to ask them. If it does not fit on one page it is not a cheat
sheet.
