#!/usr/bin/env python3
"""
update_readme.py

Scans the `solutions/` directory, parses problem metadata from `metadata.json`
or comment headers in source files, and updates README.md with summary statistics,
date completed, and an updated Markdown table sorted by date (newest to oldest).
"""

import json
import re
from pathlib import Path
from generate_chart import main as generate_chart_main

ROOT_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = ROOT_DIR / "solutions"
README_PATH = ROOT_DIR / "README.md"

DIFFICULTY_BADGES = {
    "Easy": "![Easy](https://img.shields.io/badge/Difficulty-Easy-brightgreen?style=flat-square)",
    "Medium": "![Medium](https://img.shields.io/badge/Difficulty-Medium-orange?style=flat-square)",
    "Hard": "![Hard](https://img.shields.io/badge/Difficulty-Hard-red?style=flat-square)"
}

LANG_LABELS = {
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".h": "C/C++",
    ".py": "Python",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".js": "JavaScript",
    ".ts": "TypeScript"
}


def parse_metadata_from_json(json_file: Path) -> dict:
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_metadata_from_code(code_file: Path) -> dict:
    meta = {}
    content = code_file.read_text(encoding="utf-8")
    
    id_match = re.search(r"Problem:\s*(\d+)\.\s*(.*)", content)
    url_match = re.search(r"URL:\s*(https?://[^\s]+)", content)
    diff_match = re.search(r"Difficulty:\s*(Easy|Medium|Hard)", content, re.IGNORECASE)
    topics_match = re.search(r"Topics:\s*(.*)", content)
    date_match = re.search(r"Date:\s*(.*)", content)

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
    if date_match:
        meta["date"] = date_match.group(1).strip()

    return meta


def parse_date_sort_key(date_str: str, problem_id: int):
    """
    Parses date strings like '20/08/2026' or 'X/X/2024' (DD/MM/YYYY)
    into a tuple for newest-to-oldest sorting: (-year, -month, -day, problem_id).
    """
    if not date_str:
        return (0, 0, 0, problem_id)
    
    parts = date_str.split("/")
    if len(parts) == 3:
        d_str, m_str, y_str = parts
        year = int(y_str) if y_str.isdigit() else 0
        month = int(m_str) if m_str.isdigit() else 0
        day = int(d_str) if d_str.isdigit() else 0
        return (-year, -month, -day, problem_id)
    
    return (0, 0, 0, problem_id)


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

        # Find code files (.c, .cpp, etc.)
        code_files = [f for f in folder.iterdir() if f.is_file() and f.suffix in LANG_LABELS]
        
        if not metadata and code_files:
            metadata = parse_metadata_from_code(code_files[0])

        if metadata and "id" in metadata:
            rel_folder = folder.relative_to(ROOT_DIR).as_posix()
            
            # Build clickable language buttons/links (e.g. [C], [C++])
            if code_files:
                links = []
                for f in sorted(code_files):
                    label = LANG_LABELS.get(f.suffix, "Code")
                    links.append(f"[{label}]({rel_folder}/{f.name})")
                sol_link = ", ".join(links)
            else:
                sol_link = f"[Solution]({rel_folder})"

            # Format problem ID as 4-digit padded string (e.g., 0001)
            problem_id = f"{metadata['id']:04d}"
            title = metadata.get("title", f"Problem {problem_id}")
            url = metadata.get("url", f"https://leetcode.com/problems/{folder.name.split('-', 1)[-1]}/")
            difficulty = metadata.get("difficulty", "Easy")
            date_completed = metadata.get("date", "X/X/2024")

            solutions.append({
                "id": metadata['id'],
                "id_str": problem_id,
                "title": title,
                "url": url,
                "difficulty": difficulty,
                "date": date_completed,
                "solution_link": sol_link
            })

    # Sort primarily by DATE (newest to oldest), secondarily by problem ID
    solutions.sort(key=lambda s: parse_date_sort_key(s["date"], s["id"]))
    return solutions


def generate_stats_markdown(solutions):
    total = len(solutions)
    easy = sum(1 for s in solutions if s["difficulty"] == "Easy")
    medium = sum(1 for s in solutions if s["difficulty"] == "Medium")
    hard = sum(1 for s in solutions if s["difficulty"] == "Hard")

    stats = (
        f"### Progress Summary\n\n"
        f"- **Total Solved:** `{total}`\n"
        f"- **Easy:** `{easy}`\n"
        f"- **Medium:** `{medium}`\n"
        f"- **Hard:** `{hard}`\n"
    )
    return stats


def generate_table_markdown(solutions):
    if not solutions:
        return "_No solutions added yet._\n"

    lines = [
        "| # | Title | Solution | Difficulty | Date |",
        "|---|---|---|---|---|"
    ]

    for s in solutions:
        id_str = f"`{s['id_str']}`"
        title_link = f"[{s['title']}]({s['url']})"
        sol_link = s["solution_link"]
        diff_badge = DIFFICULTY_BADGES.get(s["difficulty"], f"`{s['difficulty']}`")
        date_str = f"`{s['date']}`" if s['date'] else "`X/X/2024`"

        lines.append(f"| {id_str} | {title_link} | {sol_link} | {diff_badge} | {date_str} |")

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
    print(f"README.md successfully updated with {len(solutions)} problem(s) sorted by date.")
    
    try:
        generate_chart_main()
    except Exception as e:
        print(f"Warning: Could not regenerate chart: {e}")


if __name__ == "__main__":
    update_readme()
