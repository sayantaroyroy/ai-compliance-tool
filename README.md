# 🛡️ AI Compliance Officer - Full Stack Boilerplate

A production-ready AI SaaS starter kit. Built with **FastAPI**, **Docker**, and **Tailwind CSS**. 
Deploy a multi-modal (Text, Image, Audio) risk scanner in minutes.

## 🚀 Features
* **Multi-Modal Analysis:**
    * 📄 **Text:** NLP scanning for PII and toxicity.
    * 👁️ **Vision:** OCR (Tesseract) to read text from images.
    * 🎙️ **Audio:** Speech processing pipeline.
* **Modern UI:** Fully responsive Dark Mode interface using Tailwind CSS.
* **Dockerized:** Ready to deploy to Render, Railway, or AWS.
* **No Paid APIs:** Uses open-source libraries (Tesseract, Regex) - Zero monthly costs.
* **Monetization Ready:** AdSense placeholders and "Pro" features structure included.

## 🛠️ Tech Stack
* **Backend:** Python 3.9, FastAPI, Uvicorn
* **Frontend:** HTML5, Vanilla JS, Tailwind CSS (CDN)
* **AI/ML:** Pytesseract, Pillow, Regex
* **DevOps:** Docker, Gunicorn

## ⚡ Quick Start (Local)

1.  **Clone the repo**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/ai-compliance-tool.git](https://github.com/YOUR_USERNAME/ai-compliance-tool.git)
    cd ai-compliance-tool
    ```

2.  **Run with Docker** (Recommended)
    ```bash
    docker build -t compliance-app .
    docker run -p 8000:8000 compliance-app
    ```
    Open `http://localhost:8000` in your browser.

## ☁️ Deployment (Render.com)
1.  Fork this repo.
2.  Create a new **Web Service** on Render.
3.  Select "Docker" as the Runtime.
4.  Deploy! (Zero config required).

## 📄 License
This project is open for personal and commercial use.
