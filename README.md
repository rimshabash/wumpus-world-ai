# 🐉 Wumpus World AI

### Knowledge-Based Agent with Resolution Refutation

![Netlify Status](https://img.shields.io/badge/deployed-success-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-2.3.3-green)
![React](https://img.shields.io/badge/react-18-blue)

## 🌟 Live Demo

🎮 **Play Now:** [https://wumpus-gam.netlify.app](https://wumpus-gam.netlify.app)

---

## 📖 About The Project

Wumpus World AI is an intelligent agent that navigates a dangerous cave using **Propositional Logic** and **Resolution Refutation**. The agent receives real-time percepts (Breeze, Stench, Glitter) and uses logical inference to deduce safe paths while avoiding pits and the deadly Wumpus.

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🧠 **Knowledge-Based Agent** | Uses propositional logic for decision making |
| 📊 **Resolution Refutation Engine** | Proves safe cells using logical contradiction |
| 💨 **Dynamic Percept System** | Real-time Breeze, Stench, and Glitter detection |
| 🎮 **Dual Game Modes** | Player mode (manual) & AI mode (autonomous) |
| 📈 **Real-time Metrics** | Track inference steps, visited cells, and safe cells |
| 🎨 **Beautiful UI** | Gradient design with smooth animations |
| 📱 **Responsive Design** | Works on desktop and mobile devices |

---

## 🏗️ Architecture
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ │ │ │ │ │
│ React Frontend│────▶│ Flask Backend │────▶│ Resolution │
│ (Netlify) │◀────│ (PythonAnywhere)│◀────│ Engine │
│ │ │ │ │ │
└─────────────────┘ └─────────────────┘ └─────────────────┘

text

---

## 🛠️ Technologies Used

### Frontend
- **React 18** - UI Framework
- **Axios** - API calls
- **CSS3** - Animations & styling

### Backend
- **Flask 2.3.3** - REST API
- **Flask-CORS** - Cross-origin requests
- **Custom Resolution Engine** - Propositional logic inference

---

## 🚀 Getting Started

### Prerequisites

```bash
# Backend
pip install flask flask-cors

# Frontend
cd frontend
npm install axios
Local Development
1. Clone the repository

bash
git clone https://github.com/rimshabash/wumpus-world-ai.git
cd wumpus-world-ai
2. Run Backend Server

bash
cd backend
python app.py
# Server runs on http://localhost:5000
3. Run Frontend

bash
cd frontend
npm start
# App runs on http://localhost:3000
🎮 How to Play
👤 Player Mode
Click "Start Game" → Select "player"

Click on adjacent cells to move

Percepts guide you:

💨 Breeze = Pit nearby

👃 Stench = Wumpus nearby

✨ Glitter = Gold found!

Find the gold without falling into pits or getting eaten!

🤖 AI Mode
Click "Start Game" → Select "ai"

Watch the AI navigate using logical inference

Real-time metrics show:

Inference steps (resolution refutation calls)

Safe cells identified

Steps taken

Current percepts

📊 Game Elements
Element	Icon	Description
Agent	🤖	Your character (or AI)
Gold	💰	Goal - Collect to win
Pit	🕳️	Instant death
Wumpus	🐉	Deadly monster
Breeze	💨	Indicates adjacent pit
Stench	👃	Indicates adjacent Wumpus
🧠 How Resolution Refutation Works
The AI maintains a Knowledge Base (KB) of propositional logic clauses:

TELL operations: Add percept-based rules (e.g., Breeze → (Pit₁ ∨ Pit₂ ∨ ...))

ASK operations: Query if a cell is safe by proving ¬Pit ∧ ¬Wumpus

Resolution: Resolves clauses to find contradictions

Decision: Moves only to logically proven safe cells

📈 Inference Metrics
The inference counter increments each time:

AI queries if a cell contains a pit

AI queries if a cell contains the Wumpus

Resolution algorithm attempts to prove/disprove facts

🌐 Deployment
Backend (PythonAnywhere)
text
https://RimshaBashir.pythonanywhere.com
Frontend (Netlify)
text
https://wumpus-gam.netlify.app
🗂️ Project Structure
text
wumpus-world-ai/
├── backend/
│   ├── app.py              # Flask API & Resolution Engine
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Styling
│   │   └── index.js        # Entry point
│   ├── public/
│   │   └── index.html
│   └── package.json
└── README.md
📄 License
This project is open source and available under the MIT License.

📧 Contact
Developer: Rimsha Bashir

GitHub: @rimshabash

Project Link: https://github.com/rimshabash/wumpus-world-ai
