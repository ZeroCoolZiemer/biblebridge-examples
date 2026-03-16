import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BIBLEBRIDGE_KEY")
BASE = "https://holybible.dev/api"


def slice_range(start_index, end_index):
    r = requests.get(
        f"{BASE}/slice",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={
            "start_index": start_index,
            "end_index": end_index
        }
    )
    return r.json()


def verse_label(v):
    return f"{v['book']['name']} {v['chapter']}:{v['verse']}"


# --------------------------------------------------
# Case 1 — The Boundary Leap
# --------------------------------------------------

def case_boundary_leap():

    print("\nCase 1 — The Boundary Leap")
    print("-" * 60)
    print("Start at the very last verse of the Old Testament:")
    print("Malachi 4:6 (verse_index 23145)")
    print("Now add +1.\n")

    start_index = 23145
    end_index = start_index + 1

    result = slice_range(start_index, end_index)

    first = result["data"][0]
    last = result["data"][1]

    print(f"{first['verse_index']} → {verse_label(first)}")
    print(f"{last['verse_index']} → {verse_label(last)}\n")

    print("Explanation:")
    print("A single +1 operation crossed:")
    print("  • Malachi → Matthew")
    print("  • Old Testament → New Testament")
    print("  • ~400 years of intertestamental history")
    print("\nThe canonical boundary of the Bible becomes a simple integer increment.")


# --------------------------------------------------
# Case 2 — The Midpoint of the Bible
# --------------------------------------------------

def case_midpoint():

    print("\nCase 2 — The Midpoint of the Bible")
    print("-" * 60)

    total_verses = 31102
    midpoint = total_verses // 2

    result = slice_range(midpoint, midpoint)
    verse = result["data"][0]

    print(f"Total verses in the Bible: {total_verses}")
    print(f"Midpoint index: {midpoint}\n")

    print("Most people guess the midpoint of the Bible is somewhere in Psalms.")
    print("They're right — but the exact verse is surprising.\n")

    print(f"Midpoint verse: {verse_label(verse)}")

    print("\nExplanation:")
    print("Because every verse has a fixed coordinate,")
    print("you can jump to any percentage of the Bible instantly.")


# --------------------------------------------------
# Case 3 — Reading Plan Intersection
# --------------------------------------------------

def case_plan_overlap():

    print("\nCase 3 — When Reading Plans Collide")
    print("-" * 60)

    print("Plan A: 'Read Through Revelation'")
    print("        (last 100 verses of the Bible)")
    print("Plan B: 'Finish the New Testament'")
    print("        (last 140 verses)\n")

    plan_a_start = 31003
    plan_a_end = 31102

    plan_b_start = 30963
    plan_b_end = 31102

    overlap_start = max(plan_a_start, plan_b_start)
    overlap_end = min(plan_a_end, plan_b_end)

    result = slice_range(overlap_start, overlap_end)

    first = result["data"][0]
    last = result["data"][-1]

    print(f"Overlap begins at: {verse_label(first)}")
    print(f"Overlap ends at:   {verse_label(last)}")
    print(f"Shared verses:     {result['verse_count']}\n")

    print("Explanation:")
    print("Passage overlap becomes simple integer range math:")
    print("intersection = [max(A_start, B_start), min(A_end, B_end)]")
    print("\nNo string parsing or chapter boundary logic required.")


# --------------------------------------------------
# Case 4 — Build a 365-Day Reading Plan
# --------------------------------------------------

def case_reading_plan():

    print("\nCase 4 — Build a 365-Day Reading Plan")
    print("-" * 60)

    total_verses = 31102

    verses_per_day = total_verses // 365

    day = 100

    day_start = verses_per_day * (day - 1) + 1
    day_end = verses_per_day * day

    result = slice_range(day_start, day_end)

    first = result["data"][0]
    last = result["data"][-1]

    print("Reading plan logic:\n")

    print("verses_per_day = 31102 // 365")
    print(f"day_{day}_start = {day_start}")
    print(f"day_{day}_end   = {day_end}\n")

    print(f"Day {day} begins at: {verse_label(first)}")
    print(f"Day {day} ends at:   {verse_label(last)}")
    print(f"Verses that day:     {result['verse_count']}\n")

    print("Explanation:")
    print("A complete year-long reading plan can be generated")
    print("using only integer math and verse indexes.")
    print("No chapter lengths or book transitions required.")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("BibleBridge — Canonical Coordinate Examples")
    print("=" * 60)
    print("These examples show how Scripture becomes navigable")
    print("when every verse has a canonical coordinate.\n")

    case_boundary_leap()
    case_midpoint()
    case_plan_overlap()
    case_reading_plan()

    print("\n" + "=" * 60)
    print("Key Idea:")
    print("The Bible behaves like a continuous coordinate space.")
    print("Navigation becomes simple integer math.")
    print("=" * 60)


if __name__ == "__main__":
    main()