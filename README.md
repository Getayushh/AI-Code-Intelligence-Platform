# 🚀 AI Code Intelligence & Codebase Analysis Platform

## 📌 Overview

This project is a full-stack AI-powered system that analyzes entire codebases to detect code duplication, semantic similarity, and generate actionable insights for improving code quality.

---

## 🎯 Features

* ✅ Type 1 Clone Detection (Exact Match)
* ✅ Type 2 Clone Detection (Token-Based)
* ✅ Type 3 Clone Detection (AST-Based)
* ✅ Type 4 Clone Detection (Semantic Similarity using Embeddings)
* ✅ Clustering of similar files (DBSCAN)
* ✅ Code Quality Insights & Risk Analysis
* ✅ Upload ZIP / Analyze entire repository

---

## 🧠 Tech Stack

### Backend

* FastAPI
* Python
* scikit-learn
* sentence-transformers

### Frontend

* HTML, JavaScript

---

## 🏗️ System Architecture

User → Upload → Backend Processing → Clone Detection → Clustering → Insights → Dashboard

---

## 📂 Project Structure

```
app/
  routes/
  services/
    clone_detector/
frontend/
```

---

## ⚙️ Installation

```bash
git clone <your-repo-link>
cd ai-code-intelligence

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## ▶️ Run Backend

```bash
uvicorn app.main:app --reload
```

---

## 🌐 Run Frontend

```bash
cd frontend
python3 -m http.server 5500
```

Open:
http://localhost:5500

---

## 📊 Example Output

* Clone detection results
* Clusters of similar files
* Risk level & suggestions

---

## 🚀 Future Improvements

* CodeBERT integration
* FAISS for fast similarity search
* Multi-language support
* Better UI dashboard

---

## 👨‍💻 Author

Ayush Gupta

---
