# Sketch to 3D – AI-Powered Web Application

**Sketch to 3D** is a full-stack web application that transforms hand-drawn sketches into interactive 3D models. It combines AI-powered shape recognition and image recognition with dynamic rendering using **Three.js**, enabling users to bring their sketches to life

---

## 🖼️ Screenshots  
*(Add your screenshots or GIFs here)*  
- Input sketch upload interface
- ![Drawing Screen](https://github.com/user-attachments/assets/6a89fa13-c74c-44f1-abf1-ea211765396f)

- AI response and preview
- ![3D Model Viewer](https://github.com/user-attachments/assets/2e19f9c8-c2e7-4fd8-ad5b-7f4e0451f3ed)
---

## ✨ Features

- 🎯 **Sketch Recognition with AI**  
  Uses Azure OpenAI to analyze simple hand-drawn sketches and return detailed sketches.
  
-  **Sketch Recognition with AI**  
  Uses Azure OpenAI to analyze simple hand-drawn sketches and return detailed sketches.

- 🧩 **Dynamic Three.js Code Generation**  
  Converts AI output into real-time, browser-rendered 3D scenes using procedural logic.

- 🧠 **Modular FastAPI Backend**  
  Clean, scalable Python backend built for fast iteration and easy extension.

- 🌐 **In-Browser Visualization**  
  Fully interactive 3D viewer with rotation, zoom, and pan — no plugins or installations required.

---

## 🛠 Tech Stack

- **Frontend:** HTML5, Three.js, CSS, React-Konva
- **Backend:** Python, FastAPI, Azure OpenAI, PIL
- **Other:** REST API, Image preprocessing pipeline

---

## ⚙️ How It Works

1. User draws a basic sketch on the canvas
2. Send the image to the back-end to be processed
3. Run it through to AI's that have been prompt engineered to write refined and detailed ThreeJS code
4. The system generates Three.js code based on the structure  
5. The 3D model is rendered in-browser and ready for interaction
6. User can swap between sketch and 3d model as well add more sketches to a scene
7. User can export their 3d model and code

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/NolanS55/sketch-to-3d.git

# Backend setup
cd back-end
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend setup (if applicable)
cd front-end
npm install
npm run dev
```
---

## 📫 Contact

- **Portfolio:** [My Portfolio](https://nolan-smith-portfolio.vercel.app/)  
- **Email:** [My Email](mailto:nolan4smith@gmail.com)  
- **LinkedIn:** [My Linkiden](https://www.linkedin.com/in/nolan-smith-07a79a1a9/)
