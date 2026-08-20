# Research playbook

Read this in Phase 1, before writing prose. The aim is to reach the writing stage holding four
things: a concept spine, numbers with sources attached, worked examples you did not invent, and a
list of the misconceptions people actually hold. Without those, what comes out is a confident
summary of the topic's Wikipedia page, and a reader can tell within two pages.

## Scope the topic before researching it

Three questions, answered in writing before you search anything:

**What is inside?** Name the sub-topics the book covers. Six to fourteen concepts is a book;
thirty is a syllabus and will produce a book that teaches nothing well.

**What is adjacent, and excluded?** Write the exclusions down and put them on the front matter
page. "This book covers routing policy and does not cover model training" saves the reader from
looking for a chapter that was never coming, and it stops you from drifting into it.

**At what level?** Mid, senior, staff, or academic. The level changes everything: the same topic
at mid is mechanism-and-vocabulary, at staff it is trade-offs, failure modes, and what you would
do differently. If the reader gave you a goal ("interviewing for a senior infra role"), the level
is stated. If they did not, ask, or pick senior and say on the front matter that you did.

## The concept spine

Everything in Part II hangs off this, so build it deliberately.

For each concept, write one line: **the problem it solves.** Not what it is — what breaks without
it. `Load-aware routing` is not a concept; "requests pile up behind the slowest backend unless
routing knows the queue depth" is. A chapter that opens with the problem is a chapter the reader
remembers, because they can reconstruct the answer from the problem later, in a room, under
pressure.

Then order the spine by **dependency**, not by popularity or by how the field usually presents it.
A concept goes after everything it needs and before everything that needs it. Where the
conventional teaching order violates dependency, break with it and say why in one sentence.

## Sources, in the order worth reading

1. **Primary specifications and official documentation** for whatever is standardized or shipped.
   Cite the version. Documentation is the only class where you can quote behaviour as fact.
2. **The papers, when the topic has them.** Read the abstract, the method, and the limitations
   section. The limitations section is where the interview follow-ups live.
3. **Production write-ups and postmortems.** Engineering blogs, incident reports, "how we scaled
   X" posts. This is where the numbers come from, and numbers are what separates an answer that
   sounds studied from one that sounds experienced.
4. **Source code, when the topic is implemented in something readable.** For a claim about what
   actually happens, the code beats the docs, and where they disagree that is a trap page.
5. **Talks and long-form practitioner writing.** Best for the shape of the argument and for
   discovering which trade-offs the field genuinely disputes.
6. **Textbooks and courses.** Good for the foundations chapters and for standard notation. Weak on
   anything the last two years changed.

Record every source as you go: what it is, its date, and what claim you took from it. The sources
page at the end of the book is assembled from these notes, and reconstructing them afterwards
takes longer than keeping them.

## Numbers

A study book earns its keep on numbers. Collect them as a running table: **quantity, value, unit,
source, date, conditions.** Any number missing a unit or a source does not go in the book, because
the follow-up question is always "compared to what, and where did you get that?"

Where the honest answer is a range, write the range. Where the number depends on hardware, say
which. Where a widely repeated figure has no traceable origin, say that too: knowing that a famous
number is folklore is itself an answer worth having.

## Worked examples

Take real artifacts: configuration from official docs, a code sample from a project's own
examples, the algorithm as its paper states it, the formula with its terms defined. If you must
write illustrative pseudocode, label it as illustrative in the caption. A reader who copies a
sample and finds it does not run stops trusting the rest of the book, and they are right to.

## Misconceptions are the highest-value content

The pages a reader remembers are the ones that correct something they already believed. Hunt for
these deliberately:

- Documentation sections titled "common mistakes", "gotchas", "notes", "caveats".
- Highly-voted questions on Q&A sites: a question asked ten thousand times is a misconception with
  a large population.
- "X considered harmful" and "you probably don't need X" posts, and the rebuttals to them. Read
  both; the disagreement is often the real content.
- Errata, deprecation notices, and changelog entries that reverse earlier advice.
- Places where the vocabulary collides: two communities using one word for different things is a
  reliable source of interview cross-talk.

Five well-documented misconceptions carry a book further than twenty concepts. Each one is a trap
callout, a graded question with a tempting distractor, and usually a follow-up ladder rung.

## Prerequisites: teach only what the topic leans on

Part I fails in one of two directions: skipped, leaving a reader who cannot follow Part II, or
inflated into a generic tutorial nobody needs. The discipline that fixes both is to pair every
foundation with the sentence explaining where the topic depends on it. Teach queueing theory
because the tail-latency argument in chapter four is unreadable without it, and say so in the
chapter's first paragraph. If you cannot write that sentence, cut the chapter.

## Page budget

Pick from the reader's brief, then hold yourself to it. Pagination is a constraint that improves
prose; a page that overflows should be split or cut, never crammed.

| Topic breadth | Pages | Shape |
| --- | --- | --- |
| Narrow and well-bounded (one mechanism, one tool) | 50–80 | 4–6 chapters, one mock round |
| Standard interview topic (a subsystem, a technique family) | 90–160 | 8–12 chapters, two mock rounds |
| Broad domain (a whole discipline, e.g. system design) | 180–300 | 14–24 chapters, a mock round per format, per-part examinations |

Roughly one practice sheet per chapter, four to six graded questions per sheet page, and two or
three open drills. That ratio is what makes a 200-page book usable rather than merely long.

## Verify before you claim

- **Absence is a strong claim.** Before writing "there is no way to do X", search for X in the
  primary docs, the changelog, and the issue tracker.
- **Contested is a legitimate answer.** Where practitioners genuinely disagree, write the
  disagreement, name both positions and what each optimizes for. Interviewers ask about exactly
  these, and a reader who knows it is contested can handle either interviewer.
- **Version drift.** State versions for anything that changed recently, and put the research month
  on the cover. A topic moving fast will drift from the book within a quarter; saying so is what
  keeps the book honest rather than stale.
