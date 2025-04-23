# 🌍 AIventure

AIventure is an AI-powered travel planning web app that helps users generate personalized itineraries through natural language input. Just type in where you want to go, how long you’re staying, and your travel style — AIventure will handle the rest.

## ✨ Features

- 🧠 **Multi-agent AI System**
  - `WebSearchAgent`: Finds top-rated attractions
  - `WeatherAgent`: Checks weather to optimize indoor/outdoor plans
  - `MapsAgent`: Plans routes and transportation between stops

- 💬 **Chat-based Input**
  - ChatGPT-style interface for natural interaction
  - Accepts queries like: _"I want to visit Berlin for 3 days, and I like museums"_

- 🗺️ **Interactive Map Output (coming soon)**
  - View your trip as connected dots on a map
  - Shows travel time and recommended routes

- 🧩 **Modular Agent Architecture**
  - Easily extendable with more agents (e.g., cost estimator, event recommender)

- ⚡ Built with:
  - Next.js App Router
  - Tailwind CSS (with custom color palette)
  - `react-aria-components` for accessibility
  - TypeScript
  - Azure AI Search or OpenAI API for reasoning

---

## 📁 Project Structure
```bash
aiventure/                # Project root directory
├── app/                  # App Router directory in Next.js
│   ├── page.tsx          # Your homepage (includes chat UI)
│   └── api/plan/route.ts # API route for calling your AI Agents (POST)
├── components/           # Reusable frontend UI components
│   ├── ChatInput.tsx     # The chat input field + send button
│   ├── ChatMessageList.tsx # Shows the chat messages
│   └── icons/            # Folder for custom SVG icons (e.g. SendIcon)
├── lib/                  # Logic/helpers shared across the app
│   └── agents.ts         # AI agent pipeline logic (WebSearchAgent, etc.)
├── styles/               # Global CSS and Tailwind styles
│   └── globals.css
├── types/                # TypeScript types shared across components
├── tailwind.config.js    # Your Tailwind theme setup (e.g. colors)
└── README.md             # Documentation file (the one you're writing now)
```

## 🚀 Getting Started

### 1. Clone & Install

```bash
yarn install && yarn dev
```

create `.env.local` and I will tell u the secret