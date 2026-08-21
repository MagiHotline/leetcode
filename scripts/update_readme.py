#!/usr/bin/env python3
"""
update_readme.py

Scans the `solutions/` directory, parses problem metadata from `metadata.json`
or comment headers in `solution.cpp`, and updates README.md with summary statistics
and an updated Markdown table.
"""

import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = ROOT_DIR / "solutions"
README_PATH = ROOT_DIR / "README.md"

DIFFICULTY_BADGES = {
    "Easy": "![Easy](https://img.shields.io/badge/Difficulty-Easy-brightgreen?style=flat-square)",
    "Medium": "![Medium](https://img.shields.io/badge/Difficulty-Medium-orange?style=flat-square)",
    "Hard": "![Hard](https://img.shields.io/badge/Difficulty-Hard-red?style=flat-square)"
}


def parse_metadata_from_json(json_file: Path) -> dict:
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_metadata_from_cpp(cpp_file: Path) -> dict:
    meta = {}
    content = cpp_file.read_text(encoding="utf-8")
    
    id_match = re.search(r"Problem:\s*(\d+)\.\s*(.*)", content)
    url_match = re.search(r"URL:\s*(https?://[^\s]+)", content)
    diff_match = re.search(r"Difficulty:\s*(Easy|Medium|Hard)", content, re.IGNORECASE)
    topics_match = re.search(r"Topics:\s*(.*)", content)

    if id_match:
        meta["id"] = int(id_match.group(1))
        meta["title"] = id_match.group(2).strip()
    if url_match:
        meta["url"] = url_match.group(1).strip()
    if diff_match:
        meta["difficulty"] = diff_match.group(1).capitalize()
    if topics_match:
        topics_str = topics_match.group(1).strip()
        meta["topics"] = [t.strip() for t in topics_str.split(",") if t.strip()]

    return meta


def get_all_solutions():
    solutions = []
    if not SOLUTIONS_DIR.exists():
        return solutions

    for folder in sorted(SOLUTIONS_DIR.iterdir()):
        if not folder.is_dir():
            continue

        metadata = None
        json_file = folder / "metadata.json"
        if json_file.exists():
            try:
                metadata = parse_metadata_from_json(json_file)
            except Exception as e:
                print(f"Warning: Failed to parse {json_file}: {e}")

        cpp_file = folder / "solution.cpp"
        if not cpp_file.exists():
            cpp_files = list(folder.glob("*.cpp"))
            if cpp_files:
                cpp_file = cpp_files[0]
            else:
                cpp_file = None

        if not metadata and cpp_file and cpp_file.exists():
            metadata = parse_metadata_from_cpp(cpp_file)

        if metadata and "id" in metadata:
            rel_folder = folder.relative_to(ROOT_DIR).as_posix()
            sol_link = f"[{cpp_file.name}]({rel_folder}/{cpp_file.name})" if cpp_file else f"[Folder]({rel_folder})"
            
            # Format problem ID as 4-digit padded string (e.g., 0001)
            problem_id = f"{metadata['id']:04d}"
            title = metadata.get("title", f"Problem {problem_id}")
            url = metadata.get("url", f"https://leetcode.com/problems/{folder.name.split('-', 1)[-1]}/")
            difficulty = metadata.get("difficulty", "Easy")
            topics = metadata.get("topics", [])

            solutions.append({
                "id": metadata['id'],
                "id_str": problem_id,
                "title": title,
                "url": url,
                "difficulty": difficulty,
                "topics": topics,
                "solution_link": sol_link
            })

    solutions.sort(key=lambda x: x["id"])
    return solutions


def generate_stats_markdown(solutions):
    total = len(solutions)
    easy = sum(1 for s in solutions if s["difficulty"] == "Easy")
    medium = sum(1 for s in solutions if s["difficulty"] == "Medium")
    hard = sum(1 for s in solutions if s["difficulty"] == "Hard")

    stats = (
        f"### 📊 Progress Summary\n\n"
        f"- **Total Solved:** `{total}`\n"
        f"- 🟢 **Easy:** `{easy}`\n"
        f"- 🟡 **Medium:** `{medium}`\n"
        f"- 🔴 **Hard:** `{hard}`\n"
    )
    return stats


def generate_table_markdown(solutions):
    if not solutions:
        return "_No solutions added yet._\n"

    lines = [
        "| # | Title | Solution | Difficulty | Topics |",
        "|---|---|---|---|---|"
    ]

    for s in solutions:
        id_str = f"`{s['id_str']}`"
        title_link = f"[{s['title']}]({s['url']})"
        sol_link = s["solution_link"]
        diff_badge = DIFFICULTY_BADGES.get(s["difficulty"], f"`{s['difficulty']}`")
        topics_str = ", ".join([f"`{t}`" for t in s["topics"]]) if s["topics"] else "-"

        lines.append(f"| {id_str} | {title_link} | {sol_link} | {diff_badge} | {topics_str} |")

    return "\n".join(lines) + "\n"


def update_readme():
    if not README_PATH.exists():
        print("README.md does not exist.")
        return

    solutions = get_all_solutions()
    stats_md = generate_stats_markdown(solutions)
    table_md = generate_table_markdown(solutions)

    content = README_PATH.read_text(encoding="utf-8")

    # Replace STATS section
    stats_pattern = r"(<!-- STATS:START -->)(.*?)(<!-- STATS:END -->)"
    if re.search(stats_pattern, content, re.DOTALL):
        content = re.sub(
            stats_pattern,
            f"\\1\n{stats_md}\n\\3",
            content,
            flags=re.DOTALL
        )

    # Replace TABLE section
    table_pattern = r"(<!-- TABLE:START -->)(.*?)(<!-- TABLE:END -->)"
    if re.search(table_pattern, content, re.DOTALL):
        content = re.sub(
            table_pattern,
            f"\\1\n{table_md}\n\\3",
            content,
            flags=re.DOTALL
        )

    README_PATH.write_text(content, encoding="utf-8")
    print(f"✅ README.md successfully updated with {len(solutions)} problem(s).")


if __name__ == "__main__":
    update_readme()
