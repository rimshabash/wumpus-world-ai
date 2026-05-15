from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
from collections import deque

app = Flask(__name__)
CORS(app)

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
        self.game_over = False
        self.message = ""
        self.gold_found = False
        
        # Generate world with guaranteed path
        self.generate_guaranteed_world()
    
    def generate_guaranteed_world(self):
        """Generate world where AI can ALWAYS reach gold"""
        
        # Exactly 3 pits
        num_pits = 3
        self.pits.clear()
        
        # Create a safe path first
        safe_path = self.create_safe_path()
        
        # Place pits away from the safe path
        all_cells = []
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) not in safe_path and (i, j) != (0, 0):
                    all_cells.append((i, j))
        
        random.shuffle(all_cells)
        for i in range(min(num_pits, len(all_cells))):
            self.pits.add(all_cells[i])
        
        # Place wumpus away from safe path and start
        wumpus_positions = [c for c in all_cells if c not in self.pits and abs(c[0]-0) + abs(c[1]-0) >= 3]
        if wumpus_positions:
            self.wumpus = random.choice(wumpus_positions)
        else:
            self.wumpus = (self.rows-1, self.cols-1)
        
        # Place gold at end of safe path
        self.gold = safe_path[-1]
        
        # Mark all pits as unsafe for KB
        print(f"\n🎮 WORLD GENERATED:")
        print(f"   📍 Start: (0,0)")
        print(f"   💰 Gold at: {self.gold}")
        print(f"   🐉 Wumpus at: {self.wumpus}")
        print(f"   🕳️ Pits at: {self.pits}")
        print(f"   🛤️ Safe path length: {len(safe_path)}")
    
    def create_safe_path(self):
        """Create a guaranteed safe path from start to a far cell"""
        path = [(0, 0)]
        current = (0, 0)
        
        # Target far corner
        target = (self.rows-1, self.cols-1)
        
        # Create path using right/down moves (simple but effective)
        while current != target:
            x, y = current
            if x < self.rows - 1 and y < self.cols - 1:
                # Randomly choose right or down
                if random.choice([True, False]):
                    current = (x + 1, y)
                else:
                    current = (x, y + 1)
            elif x < self.rows - 1:
                current = (x + 1, y)
            elif y < self.cols - 1:
                current = (x, y + 1)
            
            if current not in path:
                path.append(current)
        
        return path
    
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
        
        if position == self.gold:
            percepts.append("✨ GLITTER - GOLD FOUND!")
            return percepts
        
        neighbors = self.get_neighbors(x, y)
        
        for nx, ny in neighbors:
            if (nx, ny) in self.pits:
                percepts.append("💨 Breeze")
                break
        
        for nx, ny in neighbors:
            if (nx, ny) == self.wumpus:
                percepts.append("👃 Stench")
                break
        
        return percepts if percepts else ["✅ Safe to move"]
    
    def find_path_to_gold(self):
        """Find shortest SAFE path using BFS"""
        start = self.agent
        goal = self.gold
        
        if start == goal:
            return []
        
        queue = deque([(start[0], start[1], [])])
        visited_check = set([start])
        
        while queue:
            x, y, path = queue.popleft()
            
            for nx, ny in self.get_neighbors(x, y):
                if (nx, ny) == goal:
                    return path + [(nx, ny)]
                
                if (nx, ny) not in visited_check:
                    # Only use safe cells (not pits, not wumpus)
                    if (nx, ny) not in self.pits and (nx, ny) != self.wumpus:
                        visited_check.add((nx, ny))
                        queue.append((nx, ny, path + [(nx, ny)]))
        
        return None
    
    def move_ai(self):
        """AI that ALWAYS finds gold using BFS pathfinding"""
        if self.game_over:
            return
        
        print(f"\n{'='*50}")
        print(f"🤖 AI MOVE #{self.steps + 1}")
        print(f"📍 Current: {self.agent}")
        
        # Check win
        if self.agent == self.gold:
            self.game_over = True
            self.message = "🎉 GOLD FOUND! YOU WIN! 🎉"
            self.gold_found = True
            print(f"🎉 VICTORY! Gold found at {self.agent}!")
            return
        
        # Find path to gold
        path = self.find_path_to_gold()
        
        if path and len(path) > 0:
            next_cell = path[0]
            print(f"🎯 Path found! Next: {next_cell}")
            print(f"📏 Steps to gold: {len(path)}")
            self.agent = next_cell
        else:
            # Fallback - move to any unvisited safe neighbor
            neighbors = self.get_neighbors(*self.agent)
            safe_neighbors = [n for n in neighbors if n not in self.pits and n != self.wumpus]
            unvisited = [n for n in safe_neighbors if n not in self.visited]
            
            if unvisited:
                self.agent = unvisited[0]
                print(f"⚠️ Exploring: {self.agent}")
            elif safe_neighbors:
                self.agent = safe_neighbors[0]
                print(f"🔄 Moving to safe visited: {self.agent}")
            else:
                self.game_over = True
                self.message = "😵 Stuck! (Should not happen)"
                return
        
        self.steps += 1
        self.visited.add(self.agent)
        
        print(f"✅ New position: {self.agent}")
        print(f"📊 Steps: {self.steps}, Visited: {len(self.visited)}")
        
        # Check win after move
        if self.agent == self.gold:
            self.game_over = True
            self.message = "🎉 GOLD FOUND! YOU WIN! 🎉"
            self.gold_found = True
            print(f"🎉 VICTORY! Gold found on move {self.steps}!")
    
    def move_player(self, target):
        if self.game_over:
            return False
        
        if tuple(target) in self.get_neighbors(*self.agent):
            self.agent = tuple(target)
            self.steps += 1
            self.visited.add(self.agent)
            
            if self.agent == self.gold:
                self.game_over = True
                self.message = "🎉 GOLD FOUND! YOU WIN! 🎉"
                self.gold_found = True
            
            return True
        
        return False
    
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
                    "is_safe": (i, j) not in self.pits and (i, j) != self.wumpus,
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
                elif cell["is_safe"]:
                    cell["type"] = "safe"
                
                row.append(cell)
            
            grid_data.append(row)
        
        return grid_data
    
    def get_inference_steps(self):
        return self.steps


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
        "safe_count": (world.rows * world.cols) - len(world.pits) - 1
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
