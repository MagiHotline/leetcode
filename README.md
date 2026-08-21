# 🧩 LeetCode Solutions in C++

Welcome to my LeetCode solutions repository! This repository contains clean, efficient C++ solutions to various LeetCode problems.

---

<!-- STATS:START -->
### 📊 Progress Summary

- **Total Solved:** `2`
- 🟢 **Easy:** `1`
- 🟡 **Medium:** `1`
- 🔴 **Hard:** `0`

<!-- STATS:END -->

---

## 📝 Problem List

<!-- TABLE:START -->
| # | Title | Solution | Difficulty | Topics |
|---|---|---|---|---|
| `0001` | [Two Sum](https://leetcode.com/problems/two-sum/) | [solution.cpp](solutions/0001-two-sum/solution.cpp) | ![Easy](https://img.shields.io/badge/Difficulty-Easy-brightgreen?style=flat-square) | `Array`, `Hash Table` |
| `0002` | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | [Folder](solutions/0002-add-two-numbers) | ![Medium](https://img.shields.io/badge/Difficulty-Medium-orange?style=flat-square) | `Linked List`, `Math`, `Recursion` |

<!-- TABLE:END -->

---

## 🚀 How to Add New Problems

You can automatically scaffold a new problem folder and update `README.md` using the Python helper script:

```bash
python3 scripts/new_problem.py --id 1 --title "Two Sum" --difficulty Easy --topics "Array, Hash Table"
```

Or run in **interactive mode**:

```bash
python3 scripts/new_problem.py
```

### Manual README Update

To regenerate the `README.md` statistics and problem table from existing solution files at any time, run:

```bash
python3 scripts/update_readme.py
```

---

## 📁 Repository Structure

```text
leetcode/
├── README.md
├── scripts/
│   ├── new_problem.py
│   └── update_readme.py
└── solutions/
    └── 0001-two-sum/
        ├── metadata.json
        └── solution.cpp
```
