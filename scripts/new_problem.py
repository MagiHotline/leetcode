#!/usr/bin/env python3
"""
new_problem.py

Helper CLI script to create a new LeetCode problem folder structure with starter C/C++ solution,
metadata.json, and automatically triggers update_readme.py.

Usage:
    python3 scripts/new_problem.py --id 1 --title "Two Sum" --difficulty Easy --topics "Array, Hash Table" --lang c --date "2024/X/X"
    OR
    python3 scripts/new_problem.py (Interactive mode)
"""

import argparse
import json
import re
import sys
from pathlib import Path

from update_readme import update_readme

ROOT_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = ROOT_DIR / "solutions"


def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    return slug


def create_problem(problem_id: int, title: str, difficulty: str, topics_list: list, url: str = None, lang: str = "c", date: str = "2024/X/X"):
    slug = slugify(title)
    id_padded = f"{problem_id:04d}"
    folder_name = f"{id_padded}-{slug}"
    folder_path = SOLUTIONS_DIR / folder_name

    if folder_path.exists():
        print(f"Error: Problem directory already exists at {folder_path.relative_to(ROOT_DIR)}")
        sys.exit(1)

    folder_path.mkdir(parents=True, exist_ok=True)

    if not url:
        url = f"https://leetcode.com/problems/{slug}/"

    # Normalize difficulty
    diff_map = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}
    difficulty = diff_map.get(difficulty.lower(), "Easy")

    # Write metadata.json
    metadata = {
        "id": problem_id,
        "title": title,
        "url": url,
        "difficulty": difficulty,
        "topics": topics_list,
        "date": date
    }
    with open(folder_path / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    topics_str = ", ".join(topics_list)

    if lang.lower() == "cpp" or lang.lower() == "c++":
        code_content = f"""/*
 * Problem: {problem_id}. {title}
 * URL: {url}
 * Difficulty: {difficulty}
 * Topics: {topics_str}
 * Date: {date}
 */

#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>

using namespace std;

class Solution {{
public:
    // TODO: Implement solution
}};

int main() {{
    Solution sol;
    cout << "LeetCode {problem_id}: {title}" << endl;
    return 0;
}}
"""
        (folder_path / "solution.cpp").write_text(code_content, encoding="utf-8")
    else:
        code_content = f"""/*
 * Problem: {problem_id}. {title}
 * URL: {url}
 * Difficulty: {difficulty}
 * Topics: {topics_str}
 * Date: {date}
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// TODO: Implement solution

int main() {{
    printf("LeetCode {problem_id}: {title}\\n");
    return 0;
}}
"""
        (folder_path / "solution.c").write_text(code_content, encoding="utf-8")

    print(f"Created problem scaffolding at: {folder_path.relative_to(ROOT_DIR)}")
    
    # Automatically update README
    update_readme()


def main():
    parser = argparse.ArgumentParser(description="Create a new LeetCode problem solution folder.")
    parser.add_argument("-i", "--id", type=int, help="LeetCode Problem ID (e.g., 1)")
    parser.add_argument("-t", "--title", type=str, help="Problem Title (e.g., 'Two Sum')")
    parser.add_argument("-d", "--difficulty", type=str, choices=["Easy", "Medium", "Hard", "easy", "medium", "hard"], help="Difficulty level")
    parser.add_argument("-tp", "--topics", type=str, help="Comma-separated topics (e.g., 'Array, Hash Table')")
    parser.add_argument("-u", "--url", type=str, help="LeetCode Problem URL")
    parser.add_argument("-l", "--lang", type=str, choices=["c", "cpp", "c++"], default="c", help="Language (c or cpp)")
    parser.add_argument("--date", type=str, default="X/X/2024", help="Completion date in Italian format DD/MM/YYYY (e.g., '20/08/2026' or 'X/X/2024')")

    args = parser.parse_args()

    if args.id and args.title:
        problem_id = args.id
        title = args.title
        difficulty = args.difficulty or "Easy"
        topics_list = [t.strip() for t in args.topics.split(",")] if args.topics else []
        url = args.url
        lang = args.lang
        date = args.date
    else:
        print("=== Interactive LeetCode Problem Setup ===")
        try:
            problem_id = int(input("Problem ID (e.g., 1): ").strip())
            title = input("Problem Title (e.g., Two Sum): ").strip()
            difficulty = input("Difficulty [Easy/Medium/Hard] (default: Easy): ").strip() or "Easy"
            topics_raw = input("Topics (comma separated, e.g. Array, Hash Table): ").strip()
            topics_list = [t.strip() for t in topics_raw.split(",") if t.strip()]
            lang = input("Language [c / cpp] (default: c): ").strip() or "c"
            date = input("Completion Date (default: X/X/2024): ").strip() or "X/X/2024"
            url = input(f"URL (Leave blank for default https://leetcode.com/problems/{slugify(title)}/): ").strip() or None
        except KeyboardInterrupt:
            print("\nCancelled.")
            sys.exit(0)

    create_problem(problem_id, title, difficulty, topics_list, url, lang, date)


if __name__ == "__main__":
    main()
