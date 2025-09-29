import time
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
import sys

class MindWeave:
    def __init__(self):
        self.memories = {}
        self.last_recall = {}  # FIX: initialize last_recall
        self.demo_memories()
        self.graph = nx.Graph()
        print("MindWeave ready. A small demo memory set was created.")
        print("Tip: run 'help' for commands. To use GUI visualization, ensure a display is available.")

    def demo_memories(self):
        demo_data = [
            ("I love Python.", ["programming"], "happy"),
            ("Machine learning is fascinating.", ["AI"], "excited"),
            ("Coffee is life.", ["daily"], "content"),
            ("I enjoy long walks.", ["exercise"], "relaxed"),
            ("Reading books expands the mind.", ["knowledge"], "curious")
        ]
        for text, tags, emo in demo_data:
            self.add_memory(text, tags, emo, update_graph=False)

    def add_memory(self, text, tags=None, emo=None, update_graph=True):
        mid = f"m_{hex(hash(text) & 0xffffffff)[2:]}"
        self.memories[mid] = {"text": text, "tags": tags or [], "emo": emo}
        self.last_recall[mid] = time.time()
        if update_graph:
            self.update_graph()
        print(f"Added memory {mid}")

    def update_graph(self):
        self.graph.clear()
        for mid, data in self.memories.items():
            self.graph.add_node(mid, label=data['text'])
        # Simple example: connect memories with shared tags
        mids = list(self.memories.keys())
        for i in range(len(mids)):
            for j in range(i + 1, len(mids)):
                if set(self.memories[mids[i]]['tags']) & set(self.memories[mids[j]]['tags']):
                    self.graph.add_edge(mids[i], mids[j])

    def viz(self):
        # Quick matplotlib visualization
        pos = nx.spring_layout(self.graph)
        labels = nx.get_node_attributes(self.graph, 'label')
        nx.draw(self.graph, pos, with_labels=True, labels=labels, node_size=2000, node_color='lightblue', font_size=10)
        plt.show()

    def shell(self):
        print("MindWeave — Conversational Memory Simulator")
        print("Type 'help' for commands.")
        while True:
            cmd = input("mw> ").strip().lower()
            if cmd == "exit":
                print("Exiting.")
                break
            elif cmd.startswith("add "):
                text = cmd[4:]
                self.add_memory(text)
            elif cmd == "help":
                print("Commands:")
                print("  add <text>     - Add a new memory")
                print("  viz            - Visualize memories")
                print("  exit           - Quit MindWeave")
            elif cmd == "viz":
                self.viz()
            else:
                print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    mw = MindWeave()
    mw.shell()
