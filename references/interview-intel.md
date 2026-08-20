# Interview intelligence

Read this in Phase 2, before you write a line of Part IV. This is the research that makes the
book worth more than the textbook the reader already owns: what the questions actually are, in
whose words, in which round, and what separates a passing answer from a strong one.

It is also the part easiest to fake, and faking it is the worst thing you can do here. A reader
who walks into a loop expecting the structure you invented is worse prepared than one who
expected nothing. So the whole method below is organized around one rule: **every claim about how
someone gets interviewed is either sourced or labelled as inference.**

## Source classes, in order of reliability

**1. The employer's own words.** Careers pages that describe the loop, engineering-blog posts
about how they hire, published levelling or progression frameworks, the prep material recruiters
send candidates. Reliable, and usually vague: "a systems design round" tells you a round exists,
not what gets asked in it. Use this class to fix the *structure* of the loop.

**2. Interviewers writing about what they look for.** Blog posts, conference talks, and books by
people who run the round. This is the best source for the **rubric** — the thing candidates most
want and least often find. When someone who has run 200 loops writes down what makes an answer
strong, that sentence is worth more than fifty candidate reports.

**3. Practitioner question banks and curricula.** Long-lived public repositories, well-known prep
guides, course syllabi. Good for building the *taxonomy* of question types on a topic; weak
evidence for who asks what, since they aggregate without attribution.

**4. Candidate reports.** Forum posts, Glassdoor and Blind threads, Reddit and LeetCode
discussions, personal "I interviewed at X" write-ups, recorded mock interviews. The only class
with verbatim question phrasings, and the least reliable: selection bias toward the memorable,
often years stale, occasionally invented. Useful in aggregate, dangerous individually.

**5. The primary technical literature.** Papers, RFCs, source documentation, incident write-ups.
Not interview intelligence directly, but the place the *deep* follow-ups come from, and what a
strong answer draws on. Part II needs this anyway.

## How to weigh what you find

- **Two independent accounts, or attribute the number of accounts.** "Reported by one candidate,
  early 2026" is honest and still useful. "They ask about X" from a single forum post is not.
- **Date everything.** Loops get rewritten. A round structure from three years ago is history,
  not preparation, and should be labelled as such where you use it.
- **Separate the question from the company.** A question can be real and well-attested while its
  attribution to a specific employer is thin. When in doubt, keep the question, drop the logo.
- **Prefer phrasing to paraphrase.** Collect the words the interviewer used. Reading the real
  phrasing is how the reader stops being surprised by it, and paraphrase silently sands off the
  ambiguity that the question was testing.
- **Treat "leaked" question lists as low value even when genuine.** A list without the follow-ups
  teaches recall, and every serious loop is designed to defeat recall.

## Searches worth running

Vary these across the topic's vocabulary, and read the primary result rather than the snippet.

```
"<topic>" interview questions
"<topic>" interview experience <year>
<company> "<topic>" interview loop rounds
<company> engineering blog "how we interview"
"<topic>" system design interview walkthrough
"what I look for" interviewer "<topic>"
<topic> levelling rubric senior staff engineer
site:<forum> "<topic>" onsite round
"<topic>" mock interview transcript
<topic> "common mistakes" candidates
```

If you have no web access in this session, say so on the sources page in one sentence, build the
interview chapters from what you already know, and mark that part as unsourced. A reader can
work with a labelled gap. They cannot work with a confident fiction.

## What to extract

**Verbatim questions.** Aim for 40 to 120 across the topic, depending on breadth. Keep, for each:
the exact phrasing, the round it appeared in, the seniority, the source class, and the date.

**The round structure.** How many rounds touch this topic, how long each is, what artifact is
expected (a diagram, running code, a number, a story), and whether the round is shared with other
topics. A reader who does not know the round is 45 minutes will plan a 90-minute answer.

**Follow-up chains.** The single most valuable artifact of this research. One reported opening
question plus the three follow-ups that came after it teaches more than ten standalone questions,
because the follow-ups are where the level gets decided. Reconstruct chains wherever the source
gives you more than one turn, and mark chains you had to assemble from separate accounts.

**Failure signals.** What interviewers report marking candidates down for. Usually not ignorance:
it is jumping to a design without scoping, quoting a number with no unit, name-dropping a
technique whose failure mode the candidate cannot name, or answering a question that was not
asked.

**Level calibration.** What the same question requires at mid, senior, and staff. Published
levelling frameworks plus interviewer accounts get you most of the way. Where you are inferring,
say so in the caption — a rubric table presented as fact when it is your judgement is the kind of
error a reader cannot detect.

## The taxonomy every topic needs

Sort your collected questions into these buckets and count them. The counts decide your page
budget for Part IV, and the empty buckets are usually a research gap rather than a real absence.

| Bucket | The question form | What it tests |
| --- | --- | --- |
| Recall | "What is X?" | Vocabulary. Cheap to pass, cheap to fail on nerves. |
| Mechanism | "How does X actually work?" | Whether you have read past the abstract. |
| Trade-off | "X or Y, and why?" | Judgement. The most common senior filter. |
| Design | "Build me a …" | Scoping, sequencing, numbers, failure handling. |
| Diagnosis | "It is slow / it broke. Why?" | Whether you have operated the thing. |
| Estimation | "How many …? How much …?" | Comfort with arithmetic out loud. |
| Implementation | "Write / sketch the code for …" | Whether the abstraction survives contact. |
| Experience | "Tell me about a time you …" | Evidence behind the claims on the résumé. |
| Meta | "What would you change about X?" | Taste, and whether you follow the field. |

A topic whose interviews are 70% trade-off questions needs a different book from one that is 70%
implementation. Let the counts, not habit, set the shape.

## Turning intelligence into pages

- **A ladder page per major question**, not per question. Pick the openings that recur, and give
  each one its follow-up chain with weak / solid / strong answers. This is the component readers
  come back to.
- **One annotated mock round per interview format** the topic appears in. Write the transcript
  with the interviewer's silences in it. Annotate the moments, not the content: where a candidate
  usually stalls, where narrating matters more than being right.
- **A numbers page.** Whatever quantities this topic's interviewers expect on demand — latencies,
  costs, throughputs, limits — with units, sources, and dates. Then a drill that asks for them
  from memory.
- **A failure-signal page** written as behaviour, not advice. "Candidates who open by drawing lose
  the first five minutes" beats "remember to scope".
- **A one-page cheat sheet** the reader can reread in the taxi: the openings, the numbers, the
  three sentences worth having by heart.

## What not to do

- Do not invent a company's loop, a rubric with a company's name on it, or a question attributed
  to an employer you did not find a source for.
- Do not present aggregate forum sentiment as a company's policy.
- Do not write the interview chapters from the theory. The gap between "what matters about this
  topic" and "what gets asked about this topic" is the entire reason Part IV exists; closing that
  gap with your own priors just produces a textbook with a misleading title.
- Do not let recency bias set the weighting. If the loudest recent posts are about one fashionable
  sub-question, the book still has to cover the boring 80% that gets asked every week.
