# BibleBridge Examples

Real-world Scripture API examples using [BibleBridge](https://holybible.dev) canonical verse coordinates.

These examples demonstrate deterministic Scripture infrastructure.

No AI required.

---

## What is a canonical verse coordinate?

Every verse in the Bible has a stable global index — `verse_index` — from **1 to 31,102**.

Genesis 1:1 is `1`. Revelation 22:21 is `31,102`.

This turns Scripture into a continuous coordinate space where navigation becomes simple integer math.

---

## Examples

### `beyond_book_chapter_verse.py` — Canonical Coordinate Navigation

Four cases showing what becomes possible when you stop thinking in Book → Chapter → Verse and start thinking in coordinates.

| Case | Demonstrates |
|------|-------------|
| The Boundary Leap | +1 crosses the entire Old Testament / New Testament boundary |
| The Midpoint | Jump to any percentage of the Bible instantly |
| When Reading Plans Collide | Overlap detection as integer range math |
| 365-Day Reading Plan | A full year plan with no chapter boundary logic |
```
python beyond_book_chapter_verse.py
```

**Output:**
```
============================================================
BibleBridge — Canonical Coordinate Examples
============================================================
These examples show how Scripture becomes navigable
when every verse has a canonical coordinate.


Case 1 — The Boundary Leap
------------------------------------------------------------
Start at the very last verse of the Old Testament:
Malachi 4:6 (verse_index 23145)
Now add +1.

23145 → Malachi 4:6
23146 → Matthew 1:1

Explanation:
A single +1 operation crossed:
  • Malachi → Matthew
  • Old Testament → New Testament
  • ~400 years of intertestamental history

The canonical boundary of the Bible becomes a simple integer increment.

Case 2 — The Midpoint of the Bible
------------------------------------------------------------
Total verses in the Bible: 31102
Midpoint index: 15551

Most people guess the midpoint of the Bible is somewhere in Psalms.
They're right — but the exact verse is surprising.

Midpoint verse: Psalm 103:1

Explanation:
Because every verse has a fixed coordinate,
you can jump to any percentage of the Bible instantly.

Case 3 — When Reading Plans Collide
------------------------------------------------------------
Plan A: 'Read Through Revelation'
        (last 100 verses of the Bible)
Plan B: 'Finish the New Testament'
        (last 140 verses)

Overlap begins at: Revelation 18:9
Overlap ends at:   Revelation 22:21
Shared verses:     100

Explanation:
Passage overlap becomes simple integer range math:
intersection = [max(A_start, B_start), min(A_end, B_end)]

No string parsing or chapter boundary logic required.

Case 4 — Build a 365-Day Reading Plan
------------------------------------------------------------
Reading plan logic:

verses_per_day = 31102 // 365
day_100_start = 8416
day_100_end   = 8500

Day 100 begins at: 2 Samuel 15:26
Day 100 ends at:   2 Samuel 18:21
Verses that day:     85

Explanation:
A complete year-long reading plan can be generated
using only integer math and verse indexes.
No chapter lengths or book transitions required.

============================================================
Key Idea:
The Bible behaves like a continuous coordinate space.
Navigation becomes simple integer math.
============================================================
```

### `study_group_matcher.py` — User Input Normalization & Overlap Detection

Five cases showing how a Bible study app can match users studying the same or overlapping passages — even when they write references inconsistently.

| Case | Demonstrates |
|------|-------------|
| Same passage, different formats | `Romans 8:1-4` vs `rom 8:1-4` normalize to the same span |
| Overlapping passages | Partial overlap with unique verses on each side |
| No overlap | Negative case — completely separate passages |
| Cross-book boundary | Luke 24:50-53 vs Acts 1:1-4 across the canon |
| Truly messy input | `Romans Chapter 8: 1 thru 4` vs `Rom 8.1 - 4` |
```
python study_group_matcher.py
```
**Output:**
```
============================================================
BibleBridge — User Input Normalization & Overlap Detection
============================================================

Scenario: A Bible study app receives passage references
from real users in inconsistent formats. The app needs
to match users studying the same or overlapping passages.

Case 1 — Same passage, different formats
------------------------------------------------------------
Sarah submitted: "Romans 8:1-4"
Marcus submitted: "rom 8:1-4"

Normalized:
  Sarah: Rom.8.1-Rom.8.4
  Marcus: Rom.8.1-Rom.8.4

Shared: Rom.8.1-Rom.8.4 (4 verses)

→ Identical passages. Sarah and Marcus are studying exactly the same verses.

Case 2 — Overlapping passages
------------------------------------------------------------
David submitted: "Romans 8:1-5"
Emily submitted: "Rom 8:3-10"

Normalized:
  David: Rom.8.1-Rom.8.5
  Emily: Rom.8.3-Rom.8.10

Shared: Rom.8.3-Rom.8.5 (3 verses)
Only David: Rom.8.1-Rom.8.2 (2 verses)
Only Emily: Rom.8.6-Rom.8.10 (5 verses)

→ Partial overlap — 3 shared verses. David has 2 unique, Emily has 5 unique.

Case 3 — No overlap
------------------------------------------------------------
James submitted: "Romans 8:1-4"
Rachel submitted: "Rom 8:28-39"

Normalized:
  James: Rom.8.1-Rom.8.4
  Rachel: Rom.8.28-Rom.8.39

No overlap.

→ No shared verses. James and Rachel are studying different passages.

Case 4 — Cross-book boundary (Luke → Acts)
------------------------------------------------------------
Pastor Tim submitted: "Luke 24:50-53"
Thomas submitted: "Acts 1:1-4"

Normalized:
  Pastor Tim: Luke.24.50-Luke.24.53
  Thomas: Acts.1.1-Acts.1.4

No overlap.

→ No shared verses. Pastor Tim and Thomas are studying different passages.

Case 5 — Truly messy real-world input
------------------------------------------------------------
Jennifer submitted: "Romans Chapter 8: 1 thru 4"
Kevin submitted: "Rom 8.1 - 4"

Normalized:
  Jennifer: Rom.8.1-Rom.8.4
  Kevin: Rom.8.1-Rom.8.4

Shared: Rom.8.1-Rom.8.4 (4 verses)

→ Identical passages. Jennifer and Kevin are studying exactly the same verses.

============================================================
All comparisons used a single /diff call per pair.
No custom parsing. No string matching. No lookup tables.
============================================================
```

---

## Setup
```bash
pip install requests python-dotenv
```

Create a `.env` file:
```
BIBLEBRIDGE_KEY=your_api_key_here
```

Get a **free API key** at https://holybible.dev/signup

---

## License

MIT
