import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import "./App.css";


function App() {
  const [mode, setMode] = useState(null);
  const [grid, setGrid] = useState([]);
  const [fullGrid, setFullGrid] = useState([]);
  const [steps, setSteps] = useState(0);
  const [percepts, setPercepts] = useState([]);
  const [inference, setInference] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [message, setMessage] = useState("");
  const [rows, setRows] = useState(4);
  const [cols, setCols] = useState(4);
  const [visitedCount, setVisitedCount] = useState(0);
  const [safeCount, setSafeCount] = useState(0);
  const [showFullMap, setShowFullMap] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const update = (data) => {
    console.log("Update received:", data); // Debug log
    setGrid(data.grid);
    setFullGrid(data.full_grid);
    setSteps(data.steps);
    setPercepts(data.percepts);
    setInference(data.inference);
    setVisitedCount(data.visited_count);
    setSafeCount(data.safe_count);
    
    if (data.game_over) {
      setGameOver(true);
      setMessage(data.message);
    }
  };

  const aiStep = useCallback(async () => {
    if (gameOver || isLoading) return;
    
    console.log("🤖 AI Step called");
    setIsLoading(true);
    try {
      const res = await axios.get("http://localhost:5000/ai");
      console.log("AI Response:", res.data);
      update(res.data);
    } catch (error) {
      console.error("AI step error:", error);
    }
    setIsLoading(false);
  }, [gameOver, isLoading]);

  useEffect(() => {
    if (mode === "ai" && !gameOver) {
      console.log("Starting AI mode with interval");
      const interval = setInterval(aiStep, 800);
      return () => clearInterval(interval);
    }
  }, [mode, gameOver, aiStep]);

  const init = async () => {
    setIsLoading(true);
    try {
      await axios.post("http://localhost:5000/init", {
        rows: Number(rows),
        cols: Number(cols)
      });
      
      const m = window.prompt("🎮 Choose Game Mode:\n\n1. 👤 Player Mode - Click on cells to move\n2. 🤖 AI Mode - Watch AI navigate using logic", "player");
      
      if (m && (m.toLowerCase() === "player" || m.toLowerCase() === "ai")) {
        setMode(m.toLowerCase());
        setGameOver(false);
        setMessage("");
        setInference(0); // Reset inference counter
        
        // Get initial state
        const res = await axios.get("http://localhost:5000/state");
        update(res.data);
      } else {
        alert("Please enter 'player' or 'ai'");
      }
    } catch (error) {
      console.error("Init error:", error);
    }
    setIsLoading(false);
  };

  const reset = async () => {
    setIsLoading(true);
    try {
      await axios.post("http://localhost:5000/reset", {
        rows: Number(rows),
        cols: Number(cols)
      });
      
      const res = await axios.get("http://localhost:5000/state");
      update(res.data);
      setGameOver(false);
      setMessage("");
      setInference(0);
    } catch (error) {
      console.error("Reset error:", error);
    }
    setIsLoading(false);
  };

  const move = async (i, j) => {
    if (mode !== "player" || gameOver || isLoading) return;
    
    setIsLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/move", {
        target: [i, j]
      });
      update(res.data);
    } catch (error) {
      console.error("Move error:", error);
    }
    setIsLoading(false);
  };

  const getCellContent = (cell) => {
    if (cell.is_agent) return "🤖";
    if (cell.is_gold && (showFullMap || cell.is_visited)) return "💰";
    if (cell.is_pit && (showFullMap || cell.is_visited)) return "🕳️";
    if (cell.is_wumpus && (showFullMap || cell.is_visited)) return "🐉";
    if (cell.has_breeze && cell.is_visited) return "💨";
    if (cell.has_stench && cell.is_visited) return "👃";
    if (cell.is_visited) return "✓";
    return "?";
  };

  const getCellClass = (cell) => {
    const classes = ["cell"];
    
    if (cell.is_agent) {
      classes.push("agent");
    } else if (cell.is_gold && (showFullMap || cell.is_visited)) {
      classes.push("gold");
    } else if (cell.is_pit && (showFullMap || cell.is_visited)) {
      classes.push("pit");
    } else if (cell.is_wumpus && (showFullMap || cell.is_visited)) {
      classes.push("wumpus");
    } else if (cell.is_visited) {
      classes.push("visited");
    } else if (cell.is_safe && !cell.is_visited) {
      classes.push("safe");
    } else {
      classes.push("unknown");
    }
    
    if (cell.has_breeze && cell.is_visited) classes.push("breeze");
    if (cell.has_stench && cell.is_visited) classes.push("stench");
    
    return classes.join(" ");
  };

  const displayGrid = showFullMap ? fullGrid : grid;

  return (
    <div className="app">
      <div className="header">
        <h1>🐉 Wumpus World AI</h1>
        <p className="subtitle">Knowledge-Based Agent with Resolution Refutation</p>
      </div>

      <div className="controls-panel">
        <div className="control-group">
          <label>Grid Size:</label>
          <input 
            type="number" 
            value={rows} 
            onChange={(e) => setRows(Math.min(8, Math.max(3, parseInt(e.target.value) || 4)))}
            min="3"
            max="8"
            disabled={mode !== null && !gameOver}
          />
          <span>×</span>
          <input 
            type="number" 
            value={cols} 
            onChange={(e) => setCols(Math.min(8, Math.max(3, parseInt(e.target.value) || 4)))}
            min="3"
            max="8"
            disabled={mode !== null && !gameOver}
          />
        </div>
        
        <div className="control-group">
          <button className="btn-primary" onClick={init} disabled={isLoading}>
            {isLoading ? "⏳ Loading..." : "🎮 Start Game"}
          </button>
          <button className="btn-secondary" onClick={reset} disabled={!mode || isLoading}>
            🔄 Reset
          </button>
          <button className="btn-info" onClick={() => setShowFullMap(!showFullMap)}>
            {showFullMap ? "🔒 Hide Hazards" : "🔓 Reveal Map"}
          </button>
        </div>
      </div>

      {mode && (
        <div className="dashboard">
         <div className="stats-grid">
  <div className="stat-card">
    <div className="stat-icon">🎮</div>
    <div className="stat-info">
      <div className="stat-label">Mode</div>
      <div className="stat-value">{mode === "ai" ? "🤖 AI Agent" : "👤 Player"}</div>
    </div>
  </div>
  
  <div className="stat-card">
    <div className="stat-icon">👣</div>
    <div className="stat-info">
      <div className="stat-label">Steps Taken</div>
      <div className="stat-value">{steps}</div>
    </div>
  </div>
  
  {/* This is the fixed inference card - NO inline style anymore */}
  <div className="stat-card">
    <div className="stat-icon">🧠</div>
    <div className="stat-info">
      <div className="stat-label">Inference Steps (Resolution)</div>
      <div className="stat-value">{inference}</div>
    </div>
  </div>
  
  <div className="stat-card">
    <div className="stat-icon">✅</div>
    <div className="stat-info">
      <div className="stat-label">Safe Cells Known</div>
      <div className="stat-value">{safeCount}</div>
    </div>
  </div>
  
  <div className="stat-card">
    <div className="stat-icon">📍</div>
    <div className="stat-info">
      <div className="stat-label">Visited Cells</div>
      <div className="stat-value">{visitedCount}</div>
    </div>
  </div>
  
  <div className="stat-card">
    <div className="stat-icon">👁️</div>
    <div className="stat-info">
      <div className="stat-label">Current Percepts</div>
      <div className="stat-value percepts-list">
        {percepts.map((p, i) => (
          <span key={i} className="percept-badge">{p}</span>
        ))}
      </div>
    </div>
  </div>
</div>
        </div>
      )}

      {message && (
        <div className={`message ${gameOver ? (message.includes("Win") ? "win" : "game-over") : "info"}`}>
          <span>{message}</span>
          {gameOver && (
            <button className="btn-small" onClick={reset}>Play Again</button>
          )}
        </div>
      )}

      {mode && (
        <div className="game-container">
          <div className="legend">
            <div className="legend-item"><span className="legend-box agent"></span> Agent</div>
            <div className="legend-item"><span className="legend-box visited"></span> Visited</div>
            <div className="legend-item"><span className="legend-box safe"></span> Safe (Unvisited)</div>
            <div className="legend-item"><span className="legend-box unknown"></span> Unknown</div>
            <div className="legend-item"><span className="legend-box gold"></span> Gold</div>
            <div className="legend-item"><span className="legend-box pit"></span> Pit</div>
            <div className="legend-item"><span className="legend-box wumpus"></span> Wumpus</div>
            <div className="legend-item"><span className="legend-box breeze"></span> Breeze</div>
            <div className="legend-item"><span className="legend-box stench"></span> Stench</div>
          </div>
          
          <div 
            className="grid"
            style={{ 
              gridTemplateColumns: `repeat(${cols}, minmax(70px, 90px))`,
              gap: "8px"
            }}
          >
            {displayGrid.map((row, i) =>
              row.map((cell, j) => (
                <div
                  key={`${i}-${j}`}
                  className={getCellClass(cell)}
                  onClick={() => move(i, j)}
                >
                  <div className="cell-content">
                    {getCellContent(cell)}
                  </div>
                  <div className="cell-coords">{i},{j}</div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {!mode && (
        <div className="welcome">
          <div className="welcome-content">
            <h2>🎮 Welcome to Wumpus World!</h2>
            <p>Use propositional logic and resolution refutation to navigate the dangerous cave.</p>
            <div className="features">
              <div className="feature">🧠 Knowledge-Based Agent</div>
              <div className="feature">📊 Resolution Refutation Engine</div>
              <div className="feature">💨 Dynamic Percept System</div>
              <div className="feature">🎯 Real-time Inference Metrics</div>
            </div>
            <button className="btn-large" onClick={init}>Start Adventure 🚀</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;