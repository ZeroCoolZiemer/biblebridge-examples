import os
import requests
from dotenv import load_dotenv

load_dotenv()

BIBLEBRIDGE_KEY = os.getenv("BIBLEBRIDGE_KEY")
BASE = "https://holybible.dev/api"

# --------------------------------------------------
# Two real users submit study notes to a Bible app.
# They reference the same passage differently.
# The app needs to know: are they studying the same thing?
# --------------------------------------------------

STUDY_GROUPS = [
    {
        "label": "Case 1 — Same passage, different formats",
        "user_a": {"name": "Sarah", "note": "Romans 8:1-4"},
        "user_b": {"name": "Marcus", "note": "rom 8:1-4"},
    },
    {
        "label": "Case 2 — Overlapping passages",
        "user_a": {"name": "David", "note": "Romans 8:1-5"},
        "user_b": {"name": "Emily", "note": "Rom 8:3-10"},
    },
    {
        "label": "Case 3 — No overlap",
        "user_a": {"name": "James", "note": "Romans 8:1-4"},
        "user_b": {"name": "Rachel", "note": "Rom 8:28-39"},
    },
    {
        "label": "Case 4 — Cross-book boundary (Luke → Acts)",
        "user_a": {"name": "Pastor Tim", "note": "Luke 24:50-53"},
        "user_b": {"name": "Thomas", "note": "Acts 1:1-4"},
    },
    {
        "label": "Case 5 — Truly messy real-world input",
        "user_a": {"name": "Jennifer", "note": "Romans Chapter 8: 1 thru 4"},
        "user_b": {"name": "Kevin", "note": "Rom 8.1 - 4"},
    },
]


def diff(a, b):
    r = requests.get(
        f"{BASE}/diff",
        headers={"Authorization": f"Bearer {BIBLEBRIDGE_KEY}"},
        params={"a": a, "b": b},
    )
    return r.json()


def interpret_result(result, name_a, name_b):
    overlap = result.get("overlap", False)
    intersection = result.get("intersection", {})
    only_a = result.get("only_in_a", {})
    only_b = result.get("only_in_b", {})

    if not overlap:
        return f"No shared verses. {name_a} and {name_b} are studying different passages."

    shared = intersection.get("verse_count", 0)
    extra_a = only_a.get("verse_count", 0)
    extra_b = only_b.get("verse_count", 0)

    if extra_a == 0 and extra_b == 0:
        return f"Identical passages. {name_a} and {name_b} are studying exactly the same verses."
    elif extra_a == 0:
        return f"{name_a}'s passage is fully contained inside {name_b}'s. They share {shared} verses."
    elif extra_b == 0:
        return f"{name_b}'s passage is fully contained inside {name_a}'s. They share {shared} verses."
    else:
        return f"Partial overlap — {shared} shared verses. {name_a} has {extra_a} unique, {name_b} has {extra_b} unique."


def run_case(case):
    print(f"\n{case['label']}")
    print("-" * 60)

    user_a = case["user_a"]
    user_b = case["user_b"]

    print(f'{user_a["name"]} submitted: "{user_a["note"]}"')
    print(f'{user_b["name"]} submitted: "{user_b["note"]}"')

    result = diff(user_a["note"], user_b["note"])

    if result.get("status") == "error":
        print(f"\n✗ API error: {result.get('message')}")
        return

    print("\nNormalized:")
    print(f"  {user_a['name']}: {result['a']}")
    print(f"  {user_b['name']}: {result['b']}")

    if result.get("overlap"):
        i = result["intersection"]
        print(f"\nShared: {i['osis_id']} ({i['verse_count']} verses)")

        only_a = result.get("only_in_a", {})
        only_b = result.get("only_in_b", {})

        if only_a.get("verse_count", 0) > 0:
            print(f"Only {user_a['name']}: {only_a['osis_id']} ({only_a['verse_count']} verses)")

        if only_b.get("verse_count", 0) > 0:
            print(f"Only {user_b['name']}: {only_b['osis_id']} ({only_b['verse_count']} verses)")
    else:
        print("\nNo overlap.")

    print(f"\n→ {interpret_result(result, user_a['name'], user_b['name'])}")


def main():
    print("=" * 60)
    print("BibleBridge — User Input Normalization & Overlap Detection")
    print("=" * 60)
    print()
    print("Scenario: A Bible study app receives passage references")
    print("from real users in inconsistent formats. The app needs")
    print("to match users studying the same or overlapping passages.")

    for case in STUDY_GROUPS:
        run_case(case)

    print("\n" + "=" * 60)
    print("All comparisons used a single /diff call per pair.")
    print("No custom parsing. No string matching. No lookup tables.")
    print("=" * 60)


if __name__ == "__main__":
    main()