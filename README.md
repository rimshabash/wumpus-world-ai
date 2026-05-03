# 🐉 Wumpus World AI

**Knowledge-Based Agent with Resolution Refutation**

---

## 🌟 Live Demo

**Play Now:** [https://wumpus-game-dual-mode.netlify.app](https://wumpus-game-dual-mode.netlify.app)

---

## 📖 About The Project

Wumpus World AI is an intelligent agent that navigates a dangerous cave using **Propositional Logic** and **Resolution Refutation**. The agent receives real-time percepts (Breeze, Stench, Glitter) and uses logical inference to deduce safe paths while avoiding pits and the deadly Wumpus.

---

## 🎯 Features

- 🧠 **Knowledge-Based Agent** - Uses propositional logic for decision making
- 📊 **Resolution Refutation Engine** - Proves safe cells using logical contradiction
- 💨 **Dynamic Percept System** - Real-time Breeze, Stench, and Glitter detection
- 🎮 **Dual Game Modes** - Player mode (manual) & AI mode (autonomous)
- 📈 **Real-time Metrics** - Track inference steps, visited cells, and safe cells
- 🎨 **Beautiful UI** - Gradient design with smooth animations

---

## 🛠️ Technologies Used

**Frontend:**
- React 18
- Axios
- CSS3

**Backend:**
- Flask 2.3.3
- Flask-CORS
- Custom Resolution Engine

---

## 🚀 Local Development

### Prerequisites

# Backend
pip install flask flask-cors

# Frontend
cd frontend
npm install axios

## Setup
# Clone repository
git clone https://github.com/rimshabash/wumpus-world-ai.git
cd wumpus-world-ai

# Run Backend (Terminal 1)
cd backend
python app.py

# Run Frontend (Terminal 2)
cd frontend
npm start

## How to Play
## 👤 Player Mode
Click "Start Game" → Select "player"

Click on adjacent cells to move

Find the gold without dying!

## 🤖 AI Mode
Click "Start Game" → Select "ai"

Watch the AI navigate using logic

See inference steps in real-time

## Percepts Guide

| Percept | Meaning |
|---------|---------|
| 💨 Breeze | Pit is adjacent |
| 👃 Stench | Wumpus is adjacent |
| ✨ Glitter | Gold is here! |

## Game Elements

| Element | Icon | Description |
|---------|------|-------------|
| Agent | 🤖 | Your character |
| Gold | 💰 | Goal - You win! |
| Pit | 🕳️ | Instant death |
| Wumpus | 🐉 | Deadly monster |

## 🧠 How Resolution Refutation Works
The AI maintains a Knowledge Base (KB) of propositional logic clauses:

TELL operations - Add percept-based rules

ASK operations - Query if a cell is safe

Resolution - Finds contradictions to prove safety

Decision - Moves only to proven safe cells

## 🌐 Deployment

Frontend: https://wumpus-gam.netlify.app

## 🗂️ Project Structure
text
wumpus-world-ai/

├── backend/

│   ├── app.py

│   └── requirements.txt

├── frontend/

│   ├── src/

│   │   ├── App.js

│   │   ├── App.css

│   │   └── index.js

│   ├── public/

│   │   └── index.html

│   └── package.json

└── README.md

## 📧 Contact
Developer: Rimsha Bashir
