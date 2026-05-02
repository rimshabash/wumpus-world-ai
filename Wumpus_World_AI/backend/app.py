from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import copy
import os

app = Flask(__name__)
CORS(app)

class ResolutionEngine:
    def __init__(self):
        self.clauses = []
        self.inference_count = 0
    
    def add_clause(self, clause):
        if clause and clause not in self.clauses:
            self.clauses.append(clause)
            return True
        return False
    
    def negate(self, atom):
        if atom.startswith("~"):
            return atom[1:]
        return f"~{atom}"
    
    def resolve(self, clause1, clause2):
        literals1 = set(clause1.split(" ∨ "))
        literals2 = set(clause2.split(" ∨ "))
        
        for lit1 in literals1:
            for lit2 in literals2:
                if lit1 == self.negate(lit2):
                    new_literals = (literals1 - {lit1}) | (literals2 - {lit2})
                    if not new_literals:
                        return "CONTRADICTION"
                    return " ∨ ".join(sorted(new_literals))
        return None
    
    def ask(self, query):
        self.inference_count += 1
        
        temp_clauses = copy.deepcopy(self.clauses)
        negated_query = self.negate(query)
        temp_clauses.append(negated_query)
        
        new_clauses = []
        
        while True:
            new_found = False
            
            for i in range(len(temp_clauses)):
                for j in range(i + 1, len(temp_clauses)):
                    resolvent = self.resolve(temp_clauses[i], temp_clauses[j])
                    
                    if resolvent == "CONTRADICTION":
                        return True
                    
                    if resolvent and resolvent not in temp_clauses and resolvent not in new_clauses:
                        new_clauses.append(resolvent)
                        new_found = True
            
            if not new_found:
                return False
            
            temp_clauses.extend(new_clauses)
            new_clauses = []
    
    def get_inference_count(self):
        return self.inference_count
    
    def reset(self):
        self.clauses = []
        self.inference_count = 0


class WumpusWorld:
    def __init__(self, rows=4, cols=4):
        self.rows = rows
        self.cols = cols
        self.agent = (0, 0)
        self.steps = 0
        self.pits = set()
        self.wumpus = None
        self.gold = None
        self.visited = set([(0, 0)])
        self.safe_cells = set([(0, 0)])
        self.resolution_engine = ResolutionEngine()
        self.game_over = False
        self.message = ""
        self.gold_found = False
        
        self.generate_world()
        self.initialize_kb()
    
    def generate_world(self):
        num_pits = max(1, int(self.rows * self.cols * 0.2))
        while len(self.pits) < num_pits:
            p = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
            if p != (0, 0):
                self.pits.add(p)
        
        while True:
            w = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
            if w not in self.pits and w != (0, 0):
                self.wumpus = w
                break
        
        while True:
            g = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
            if g not in self.pits and g != self.wumpus and g != (0, 0):
                self.gold = g
                break
    
    def initialize_kb(self):
        self.resolution_engine.reset()
        self.resolution_engine.add_clause(f"~P_{self.agent[0]}_{self.agent[1]}")
        self.resolution_engine.add_clause(f"~W_{self.agent[0]}_{self.agent[1]}")
    
    def get_neighbors(self, x, y):
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        neighbors = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                neighbors.append((nx, ny))
        return neighbors
    
    def get_percepts(self, position=None):
        if position is None:
            position = self.agent
        
        x, y = position
        percepts = []
        neighbors = self.get_neighbors(x, y)
        
        for nx, ny in neighbors:
            if (nx, ny) in self.pits:
                percepts.append("💨 Breeze")
                break
        
        for nx, ny in neighbors:
            if (nx, ny) == self.wumpus:
                percepts.append("👃 Stench")
                break
        
        if position == self.gold:
            percepts.append("✨ Glitter")
        
        return percepts if percepts else ["❌ None"]
    
    def update_kb_with_percepts(self):
        x, y = self.agent
        percepts = self.get_percepts()
        neighbors = self.get_neighbors(x, y)
        
        has_breeze = any("Breeze" in p for p in percepts)
        if has_breeze:
            pit_literals = [f"P_{nx}_{ny}" for nx, ny in neighbors]
            if pit_literals:
                clause = f"~Breeze_{x}_{y} ∨ {' ∨ '.join(pit_literals)}"
                self.resolution_engine.add_clause(clause)
                self.resolution_engine.add_clause(f"Breeze_{x}_{y}")
        else:
            for nx, ny in neighbors:
                clause = f"~P_{nx}_{ny}"
                self.resolution_engine.add_clause(clause)
                self.safe_cells.add((nx, ny))
        
        has_stench = any("Stench" in p for p in percepts)
        if has_stench:
            wumpus_literals = [f"W_{nx}_{ny}" for nx, ny in neighbors]
            if wumpus_literals:
                clause = f"~Stench_{x}_{y} ∨ {' ∨ '.join(wumpus_literals)}"
                self.resolution_engine.add_clause(clause)
                self.resolution_engine.add_clause(f"Stench_{x}_{y}")
        else:
            for nx, ny in neighbors:
                clause = f"~W_{nx}_{ny}"
                self.resolution_engine.add_clause(clause)
                self.safe_cells.add((nx, ny))
        
        self.resolution_engine.add_clause(f"~P_{x}_{y}")
        self.resolution_engine.add_clause(f"~W_{x}_{y}")
        self.safe_cells.add((x, y))
    
    def is_cell_safe(self, x, y):
        pit_query = f"P_{x}_{y}"
        pit_exists = self.resolution_engine.ask(pit_query)
        
        wumpus_query = f"W_{x}_{y}"
        wumpus_exists = self.resolution_engine.ask(wumpus_query)
        
        is_safe = not pit_exists and not wumpus_exists
        
        if is_safe:
            self.safe_cells.add((x, y))
        
        return is_safe
    
    def move_ai(self):
        if self.game_over:
            return
        
        self.update_kb_with_percepts()
        self.visited.add(self.agent)
        
        neighbors = self.get_neighbors(*self.agent)
        
        safe_moves = []
        for nx, ny in neighbors:
            if self.is_cell_safe(nx, ny):
                safe_moves.append((nx, ny))
        
        if safe_moves:
            unvisited = [m for m in safe_moves if m not in self.visited]
            if unvisited:
                self.agent = random.choice(unvisited)
            else:
                self.agent = random.choice(safe_moves)
        elif neighbors:
            self.agent = random.choice(neighbors)
        else:
            return
        
        self.steps += 1
        self.visited.add(self.agent)
        self.check_game()
    
    def move_player(self, target):
        if self.game_over:
            return False
        
        if tuple(target) in self.get_neighbors(*self.agent):
            self.agent = tuple(target)
            self.steps += 1
            self.visited.add(self.agent)
            self.check_game()
            return True
        
        return False
    
    def check_game(self):
        if self.agent in self.pits:
            self.game_over = True
            self.message = "💀 You fell into a pit! Game Over!"
        elif self.agent == self.wumpus:
            self.game_over = True
            self.message = "🐉 The Wumpus got you! Game Over!"
        elif self.agent == self.gold and not self.gold_found:
            self.gold_found = True
            self.game_over = True
            self.message = "🎉 Congratulations! You found the GOLD! You Win! 🎉"
    
    def get_grid_state(self, reveal_all=False):
        grid_data = []
        
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                percepts_at_cell = self.get_percepts((i, j))
                
                cell = {
                    "type": "unknown",
                    "is_agent": False,
                    "is_visited": (i, j) in self.visited,
                    "is_safe": (i, j) in self.safe_cells,
                    "is_pit": (i, j) in self.pits,
                    "is_wumpus": (i, j) == self.wumpus,
                    "is_gold": (i, j) == self.gold,
                    "has_breeze": any("Breeze" in p for p in percepts_at_cell),
                    "has_stench": any("Stench" in p for p in percepts_at_cell),
                    "has_glitter": any("Glitter" in p for p in percepts_at_cell)
                }
                
                if (i, j) == self.agent:
                    cell["type"] = "agent"
                    cell["is_agent"] = True
                elif reveal_all and (i, j) == self.gold:
                    cell["type"] = "gold"
                elif reveal_all and (i, j) in self.pits:
                    cell["type"] = "pit"
                elif reveal_all and (i, j) == self.wumpus:
                    cell["type"] = "wumpus"
                elif (i, j) in self.visited:
                    cell["type"] = "visited"
                elif (i, j) in self.safe_cells:
                    cell["type"] = "safe"
                
                row.append(cell)
            
            grid_data.append(row)
        
        return grid_data
    
    def get_inference_steps(self):
        return self.resolution_engine.get_inference_count()


world = WumpusWorld()


@app.route("/init", methods=["POST"])
def init():
    global world
    data = request.json
    world = WumpusWorld(data.get("rows", 4), data.get("cols", 4))
    return jsonify({"status": "ok"})


@app.route("/move", methods=["POST"])
def move():
    world.move_player(request.json["target"])
    return jsonify(response())


@app.route("/ai", methods=["GET"])
def ai():
    world.move_ai()
    return jsonify(response())


@app.route("/reset", methods=["POST"])
def reset():
    global world
    data = request.json
    world = WumpusWorld(data.get("rows", 4), data.get("cols", 4))
    return jsonify(response())


@app.route("/state", methods=["GET"])
def state():
    return jsonify(response())


def response():
    return {
        "grid": world.get_grid_state(False),
        "full_grid": world.get_grid_state(True),
        "steps": world.steps,
        "percepts": world.get_percepts(),
        "inference": world.get_inference_steps(),
        "game_over": world.game_over,
        "message": world.message,
        "gold_found": world.gold_found,
        "visited_count": len(world.visited),
        "safe_count": len(world.safe_cells)
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)