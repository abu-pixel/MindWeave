# mindweave.py — MindWeave: Living Memory Network with Particle Effects
import matplotlib
try:
    matplotlib.use("Qt5Agg")
except Exception:
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random
import uuid
import time
import threading
import numpy as np

# ---------------------------
# Memory & Graph Management
# ---------------------------
class MindWeave:
    def __init__(self):
        self.G = nx.Graph()
        self.demo_memories()
        self.fig, self.ax = plt.subplots(figsize=(10,6))
        plt.ion()
        self.last_recall = {}      # node: last recall time
        self.dreamed_edges = set() # edges created by dreams
        self.edge_decay = {}       # edge: last activity timestamp
        self.running = True
        self.particles = []        # list of moving particles along edges
        self.visualize_thread = threading.Thread(target=self.auto_visualize, daemon=True)
        self.visualize_thread.start()
        print("MindWeave ready. Magical memory network active!")

    def demo_memories(self):
        demo = [
            ("Met Anna at the coffee shop yesterday. We discussed large language models and ethics.", ['anna','meeting','ai'], 'curiosity'),
            ("Bought a small plant, kept it on my desk. Water weekly.", ['plant','habit'], 'joy'),
            ("Learned about reinforcement learning last week; feeling excited to experiment.", ['rl','learning'], 'excite'),
            ("Phone battery drained unexpectedly during a meeting.", ['phone','bug'], 'annoyance'),
            ("Favorite dessert: dark chocolate and coffee.", ['food','preference'], 'joy')
        ]
        for text, tags, emo in demo:
            self.add_memory(text, tags, emo, update_graph=False)

    def add_memory(self, text, tags=None, emotion=None, update_graph=True):
        mid = "m_" + uuid.uuid4().hex[:10]
        self.G.add_node(mid, text=text, tags=tags or [], emotion=emotion, strength=1.0)
        self.last_recall[mid] = time.time()
        print(f'Added memory {mid}')
        return mid

    def list_memories(self, top_n=None):
        nodes = sorted(self.G.nodes(data=True), key=lambda x: -x[1]['strength'])
        if top_n: nodes = nodes[:top_n]
        for n, data in nodes:
            print(f"{n} - strength={data['strength']:.3f} tags={data['tags']} emotion={data['emotion']}\n  {data['text']}")

    def recall(self, query):
        matching = []
        now = time.time()
        for n, data in self.G.nodes(data=True):
            if query.lower() in data['text'].lower() or any(query.lower() in t for t in data['tags']):
                matching.append(n)
                self.last_recall[n] = now
        if matching:
            for idx, n in enumerate(matching, 1):
                data = self.G.nodes[n]
                print(f"[{idx}] id={n} strength={data['strength']:.3f} tags={data['tags']} emotion={data['emotion']}\n    {data['text']}")
        else:
            print("No relevant memories found.")
        return matching

    def dream(self, n=1):
        now = time.time()
        self.dreamed_edges.clear()
        for _ in range(n):
            if len(self.G.nodes) < 2: continue
            n1, n2 = random.sample(self.G.nodes, 2)
            self.link(n1, n2)
            self.dreamed_edges.add((n1,n2))
            self.edge_decay[(n1,n2)] = now
            self.edge_decay[(n2,n1)] = now
            print(f"Dream created: {n1} linked to {n2}")

    def link(self, id1, id2):
        self.G.add_edge(id1, id2)
        now = time.time()
        self.edge_decay[(id1,id2)] = now
        self.edge_decay[(id2,id1)] = now

    # ---------------------------
    # Particle animation helpers
    # ---------------------------
    def create_particles(self):
        self.particles.clear()
        for u,v in self.G.edges:
            if random.random() < 0.3:  # 30% chance to create a particle per edge
                self.particles.append({'edge':(u,v), 'pos':0.0, 'speed':0.02 + random.random()*0.03})

    def update_particles(self):
        new_particles = []
        for p in self.particles:
            p['pos'] += p['speed']
            if p['pos'] < 1.0:
                new_particles.append(p)
        self.particles = new_particles

    # ---------------------------
    # Visualization
    # ---------------------------
    def auto_visualize(self):
        while self.running:
            self.visualize()
            time.sleep(0.05)

    def visualize(self):
        self.ax.clear()
        pos = nx.spring_layout(self.G, seed=42)

        now = time.time()
        # Node colors: glow recently recalled
        node_colors = []
        for n in self.G.nodes:
            age = now - self.last_recall.get(n, now)
            glow = min(1.0, max(0.3, 1 - age/10))  # glow fades after 10 sec
            node_colors.append((glow, 0.5*glow, 1.0*glow))  # blueish glow

        # Edge colors: green for dreamed edges, fade others
        edge_colors = []
        for e in self.G.edges:
            last = self.edge_decay.get(e, now)
            age = now - last
            fade = max(0.1, 1 - age/30)
            if e in self.dreamed_edges or (e[1],e[0]) in self.dreamed_edges:
                edge_colors.append((0, fade, 0))
            else:
                edge_colors.append((0.5*fade,0.5*fade,0.5*fade))

        nx.draw(self.G, pos, ax=self.ax, with_labels=True,
                node_color=node_colors, edge_color=edge_colors,
                node_size=1500, font_size=9)
        nx.draw_networkx_labels(self.G, pos, labels={n:self.G.nodes[n]['text'][:10] for n in self.G.nodes()}, font_size=8)

        # Particle animation along edges
        self.create_particles()
        self.update_particles()
        for p in self.particles:
            u,v = p['edge']
            x = pos[u][0] + p['pos'] * (pos[v][0]-pos[u][0])
            y = pos[u][1] + p['pos'] * (pos[v][1]-pos[u][1])
            self.ax.plot(x, y, 'ro', markersize=6)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

# ---------------------------
# Interactive Shell
# ---------------------------
def shell():
    mw = MindWeave()
    while True:
        try:
            cmd = input("mw> ").strip()
            if not cmd: continue
            if cmd in ('exit','quit'):
                mw.running=False
                print("Exiting.")
                break
            parts = cmd.split()
            if parts[0] == 'help':
                print("""\nMindWeave commands:
  help         - show this help
  add <text>   - add memory
  list         - list memories
  recall <q>   - recall memories (glow)
  dream [n]    - create dreams (edges highlight + particles)
  link <id1> <id2> - connect memories
  exit/quit    - quit\n""")
            elif parts[0]=='add':
                text = cmd[len('add '):].strip('"')
                mw.add_memory(text)
            elif parts[0]=='list':
                mw.list_memories()
            elif parts[0]=='recall':
                query = cmd[len('recall '):]
                mw.recall(query)
            elif parts[0]=='dream':
                n = int(parts[1]) if len(parts)>1 else 1
                mw.dream(n)
            elif parts[0]=='link':
                mw.link(parts[1], parts[2])
            else:
                print("Unknown command. Type 'help'.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    shell()
