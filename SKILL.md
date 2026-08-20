---
name: topic-to-book
description: >-
  Turn a topic and a goal into a self-contained, interactive HTML study book with first-principles
  theory, SVG figures, practice sheets, interview follow-up ladders, mock rounds, flashcards, an
  examination, and readiness tracking. Research both the technical material and how the topic is
  actually assessed. Use for interview preparation, deep study, quizzes, courses, curricula,
  question banks, revision guides, cheat sheets, or requests to learn a subject thoroughly. Do not
  use for documentation about one specific codebase; use a repository-focused workflow instead.
---

# Topic to Book

You are producing a **book**: a paginated, self-contained HTML file that takes a reader from
knowing a topic vaguely to being able to answer questions on it under pressure, out loud, with
numbers. Not a summary, not a slide deck, not a wall of scrolling text, and not a list of
questions without the teaching that makes them answerable.

Two things make this good, and neither is the design.

**It is researched twice.** Once for the technical material, from primary sources, with numbers
that carry units and citations. Once for the interview reality: what actually gets asked on this
topic, in whose words, in which round, and what separates a passing answer from a strong one.
Skip the second research pass and you have written a textbook with a misleading cover.

**The questions can catch a confident misunderstanding.** A practice sheet whose questions a
reader can pass without having read the chapter is decoration. Every distractor should be
something a reader might genuinely believe on the way in.

## Phase 0. Read the brief

The reader gives you a goal and a topic — "prep me for LLM router interviews", "system design,
senior backend", "teach me consistency models properly". From that, fix five things:

| | Where it comes from |
| --- | --- |
| **Topic scope** | Their words, narrowed by you: name what is in, and name what is adjacent and excluded. |
| **Goal** | Interview at a specific place, interviews generally, or study for its own sake. This changes Part IV entirely. |
| **Level** | Mid, senior, staff, academic. If unstated, ask — it is the one question worth interrupting for, because it changes every chapter. |
| **Time** | Days until the interview, if there is one. It sets the study routes on the how-to-use page. |
| **Page budget** | From the topic's breadth: 50–80 narrow, 90–160 standard, 180–300 for a whole domain. |

Ask at most two questions, and only about level and target. Infer the rest and state the
inference on the front matter page. Then say what you are about to build, in two sentences, and
start; do not hold a 200-page build behind a conversation.

## Phase 1. Research the topic

Read `references/research-playbook.md` before searching. It covers scoping, building the concept
spine as problems rather than definitions, source classes worth reading in order, how to collect
numbers so they survive a follow-up question, and how to hunt misconceptions deliberately.

The short version: arrive at the writing stage with a **concept spine** of six to fourteen ideas
each stated as the problem it solves, **numbers with units and sources**, **worked examples you
did not invent**, and a list of **misconceptions** people actually hold. Five well-documented
misconceptions carry a book further than twenty concepts, because they are what a reader
remembers and where the best questions come from.

## Phase 2. Find out how people are actually grilled on it

This is the phase that makes the book worth more than the reader's textbook, and the one most
guides omit. Read `references/interview-intel.md`.

Use your web search and fetch tools properly here: employer descriptions of their loops,
interviewers writing about what they look for, practitioner question banks, candidate reports,
and the primary literature the deep follow-ups come from. Extract verbatim question phrasings,
the round structure, **follow-up chains** rather than standalone questions, the failure signals
interviewers name, and what the same question requires at each level.

Two rules are absolute:

- **Never invent a loop, a rubric, or a question attributed to a company.** Two independent
  accounts, or say how many accounts it rests on and when.
- **If you have no research tools in this session, say so on the sources page in one sentence**
  and mark Part IV as unsourced. A labelled gap is workable; a confident fiction is not.

Sort what you find into the question taxonomy in the reference and *count* it. A topic whose
interviews are mostly trade-off questions needs a different book from one that is mostly
implementation, and the counts, not habit, should set the shape.

## Phase 3. Plan before you build

Write the outline down: parts, chapters, the pages inside each chapter, and where the practice
sheets, ladders, mock rounds, and examinations fall. A structure that works for most topics:

| Part | Contains |
| --- | --- |
| Front matter | Cover, contents, how to use this book with study routes by time available. |
| I · Ground truth | Only the foundations the topic leans on, each paired with the sentence saying where it leans. |
| II · The mechanisms | The concept spine, problem-then-answer, one to three pages per concept, a figure each. |
| III · The trade-off space | Comparisons, when-to-use-what, the numbers page, what the field genuinely disputes. |
| IV · How you will be grilled | The taxonomy with counts, follow-up ladders, failure signals, level signals. |
| V · Mock rounds | One annotated transcript per interview format, timed. |
| Appendices | Cheat sheet, flashcards, final examination, answer key, readiness, sources. |

Then hold the ratios: **a practice sheet after every chapter**, four to six graded questions per
sheet page plus two or three open drills, one figure per concept, one ladder per recurring
opening question. Chapters get numbers; nothing else does.

For a book over 120 pages, show the reader the outline in your reply — a compact list, not a
document — then build without waiting. They can redirect a chapter later; they cannot review 200
pages of prose you have not written yet.

## Phase 4. Build it

Write chapters as **fragment files** and assemble them. Read `references/page-types.md` for the
fragment conventions, the markup of every component, and how much text fits on a page.
`references/figure-patterns.md` has the SVG idioms: pipelines, trade-off axes, layered stacks,
feedback loops, timelines with lanes, numbers-as-figures, before-and-after spreads.

```bash
python3 scripts/assemble_book.py chapters/ -o book.html --title "The Title" --book-id topic-slug
```

The assembler concatenates fragments in filename order and writes the contents page with page
numbers counted from the assembled result, so the index cannot drift. `assets/book-shell.html`
carries the paging, both grounds, the quiz engine, the self-rating drills, the flashcard deck,
the timer, the readiness meter, copy buttons, and the jump palette. Do not re-derive any of it.

Three things worth care while writing:

**Every figure must be redrawable on a whiteboard in sixty seconds.** The reader is going to
reproduce it in front of a stranger, not admire it. And put the insight in the layout: if the
point is that the cache sits after authorization, draw it after authorization.

**Write the theory for someone who will be asked about it out loud.** Define each term the first
time it appears, because an interviewer will use the term and expect the reader to own it. Attach
the number to the claim. Where the field disagrees, say it disagrees and name what each side
optimizes for — a reader who knows a question is contested can handle either interviewer.

**Say the sentence they should say.** A `.box.say` holds a line phrased for speech, not for print.
One or two per chapter, no more, or they stop reading them.

If you have subagents available and the book is long, chapters can be drafted in parallel, but
only under a strict contract: hand each one the research notes verbatim, the relevant page-types
and figure-patterns references, its chapter's concept spine entries, and its sheet's question
budget. Then read every fragment yourself for voice and for claims the research does not support.
An unreviewed parallel draft is where invented numbers get in.

## Designing the questions

The questions are the book's spine, not its garnish. Budget roughly **one graded question per two
pages**, plus the open drills, plus the final examination.

What makes a question worth asking:

- **Draw it from a misconception or a trap.** If practitioners routinely confuse two mechanisms,
  that is a question, and the reader who skimmed will answer it wrong.
- **Prefer consequences to definitions.** "What is a scope?" tests recall. "You forget to pass
  `handle=`. What breaks, and what still works?" tests understanding.
- **Make every distractor tempting.** The wrong answers should be what the reader believed
  *before* the chapter corrected them.
- **Explain why the distractor was tempting**, not only why the answer is right.

Then the two components a multiple-choice quiz cannot cover:

**Open drills** (`.fr`) are answered out loud from memory, with a model answer to check against
and a miss/shaky/solid self-rating that persists. Phrase the prompt the way an interviewer would
phrase it, and in the model answer say what a strong answer contains *in the order it says it*,
plus the omission that costs the point. Two or three per practice sheet.

**Follow-up ladders** teach the shape of the conversation: an opening question, then the three
follow-ups that come after it, each with what weak, solid, and strong answers sound like. Readers
come back to these pages more than any other, because nowhere else tells them what happens after
the first answer.

Give every radio group a name unique across the whole book and every drill a unique `data-id` —
sharing either silently breaks grading and progress. The validator fails on both.

## Phase 5. Validate, screenshot, deliver

```bash
python3 scripts/validate_book.py book.html
```

It checks tag balance, that no Mermaid survived, that every colour is greyscale, that both grounds
are defined, that the contents page's numbers match where pages actually are, that no chapter went
without practice, that every question's correct answer is among its options and no two questions
share a radio name, that drills and cards have unique ids, and that no page is dangerously
overstuffed. It also fails on leftover placeholders, which is the mistake that most embarrasses a
finished book.

```bash
python3 scripts/shoot_pages.py book.html --out shots --pages 1,24,40 --theme dark
python3 scripts/shoot_pages.py book.html --out shots --pages 24 --graded    # sheets pre-graded
```

Shoot at least one figure page and one practice sheet before delivering: a label drifting outside
its box in an SVG is invisible in source and obvious on screen.

Then deliver. If your host can publish HTML artifacts, publish it and hand over the URL;
otherwise write the file and give the path. The book is a single file with no external requests,
so any browser opens it. Set the `<title>`, and say plainly what you could not verify — if you
never saw a page render, say the paging feel is unverified. That sentence costs nothing and
protects the reader's trust in everything else.

## The sources page is not optional

End with sources: where the theory came from with dates, where the interview intelligence came
from and how many accounts each claim rests on, which parts are your inference rather than
reported fact, and the month the research was done. Interview loops get rewritten and fast-moving
topics drift within a quarter. Saying so is what makes the book honest rather than stale.

## Failure modes

- **Writing before researching the interview.** The most common failure: a competent textbook with
  a quiz stapled on, and no idea what actually gets asked.
- **Inventing interview specifics.** A fabricated round structure or a question with a company's
  name on it is worse than nothing, because the reader will plan around it.
- **Questions with obvious answers.** If a reader can pass the sheets without reading the
  chapters, the sheets are decoration.
- **Numbers without units or sources.** The follow-up is always "compared to what, and where did
  you get that?" A book that cannot answer it teaches a habit that fails in the room.
- **A concept tour instead of a spine.** Listing what exists is not teaching what it is for. Each
  chapter opens with the problem, then the answer.
- **Overfilling pages.** Pagination is the constraint that makes this format read well. Split it.
- **Reaching for Mermaid** because a figure is hard to draw. Draw it; `figure-patterns.md` has the
  shape you need.

## Bundled resources

- `references/research-playbook.md`: scoping, the concept spine, sources, numbers, misconceptions,
  page budgets. Phase 1.
- `references/interview-intel.md`: how to research the way a topic is actually interviewed, how to
  weigh sources, the question taxonomy, and the honesty rules. Phase 2.
- `references/page-types.md`: the fragment workflow and copy-ready markup for every page type and
  component. Phase 4.
- `references/figure-patterns.md`: SVG idioms for book figures. Phase 4.
- `assets/book-shell.html`: tokens, paging, quiz engine, self-rating drills, flashcards, timer,
  readiness meter, copy buttons, jump palette. Every book starts here.
- `scripts/assemble_book.py`: splice fragments into the shell and write the contents page.
- `scripts/validate_book.py`: pre-publish structural checks. Phase 5.
- `scripts/shoot_pages.py`: screenshot specific pages in either ground. Phase 5.
