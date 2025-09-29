# README.md

# MindWeave

MindWeave is a **Living Memory Network** simulator written in Python. It creates a dynamic, interactive memory graph where nodes represent memories, edges represent associations, and visual effects display memory decay, dreams, and information flow.

## Features

* Add memories with `add "text"`
* Recall memories with `recall <query>` (matching nodes glow)
* Create dreams with `dream` (auto-highlights edges)
* Link memories with `link <id1> <id2>`
* Live auto-updating GUI visualization with animated decay, glowing effects, and particle flow
* Save/load memory graphs with JSONL
* Export memory summary to CSV

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/abu-pixel/MindWeave.git
   cd MindWeave
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the simulator:

   ```bash
   python mindweave.py
   ```

## Commands

* `add "text"` — add a memory
* `list` — list top memories
* `recall <query>` — recall matching memories (glow effect)
* `dream [n]` — create dreams (default 1)
* `link <id1> <id2>` — connect memories
* `save <path.jsonl>` — save memory graph
* `load <path.jsonl>` — load memory graph
* `export_csv <path.csv>` — export memory summary
* `exit` — quit the program

## Notes

* Multi-word arguments must be in quotes.
* GUI auto-updates when memories change.

---

# requirements.txt

```
networkx
matplotlib
pandas
PyQt5
```
