# 🏙️ CivicPulse

**CivicPulse** is an advanced, AI-powered civic complaint management and analytics platform. It bridges the gap between residents and city administrators by leveraging Generative AI to streamline issue reporting, cluster community problems, and provide actionable insights through real-time dashboards.

### 🌐 Live Demo

Try out the deployed application: **[CivicPulse App](https://civic-pulse1.streamlit.app)**

> **Admin Access Credentials:**
>
> - **Username:** `admin`
> - **Password:** `1234`

---

## 📜 Table the Contents

- [About](#-about)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Getting Started](#-getting-started)

---

## 💡 About

CivicPulse utilizes modern Large Language Models (LLMs) and vector search to transform how civic issues are tracked and resolved. Unlike traditional ticketing systems, CivicPulse understands the _context_ of complaints, automatically grouping similar issues (clustering) and allowing administrators to "chat" with their data to uncover trends.

---

## 🚀 Key Features

### 👤 Resident Portal

- **Seamless Reporting**: User-friendly interface for reporting complaints with severity classification.
- **Status Tracking**: Real-time updates on complaint resolution (Pending, Open, Resolved).

### 🛡️ Admin Dashboard

- **Kanban Workflow**: Column-based complaint lifecycle management, using action buttons to move issues between Pending, Resolved, and Junked states.
- **Hyper-Local Analytics**:
  - **Block-Level Summaries**: AI-generated summaries of issues specific to residential blocks.
  - **Trend Analysis**: Visual breakdowns by category, severity, and location.
- **Cluster Analysis**: Unsupervised Machine Learning (UMAP + DBSCAN) to detect and group systemic community themes from unstructured text.
- **AI Assistant**: A RAG-based (Retrieval-Augmented Generation) chatbot that answers natural language queries about the complaints database.

---

## 🛠️ Tech Stack

**Core Infrastructure**

- **Language**: Python 3.10+
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Database**: [MongoDB Atlas](https://www.mongodb.com/atlas) (Vector Search enabled)

**Artificial Intelligence & ML**

- **LLM Provider**: [Google Gemini](https://ai.google.dev/) (Gemini Flash, Embedding-001)
- **Clustering**: Scikit-learn (DBSCAN), UMAP
- **Libraries**: `google-genai`, `pymongo`, `pandas`, `plotly`

---

## 📸 Screenshots

  <img width="1797" height="536" alt="1homepage" src="https://github.com/user-attachments/assets/177aeeb1-0885-49b7-974f-e1de3f05a8f2" />
  <img width="1777" height="725" alt="2residentportal" src="https://github.com/user-attachments/assets/67dc97b1-aef2-42c2-89c6-2eeaab953f98" />
  <img width="1792" height="827" alt="3 1admindasboard" src="https://github.com/user-attachments/assets/8ffdc6b0-d440-44f8-bd15-1d8a8be03eec" />
  <img width="1477" height="692" alt="3 2admindasboard" src="https://github.com/user-attachments/assets/ed9f2038-3366-4f58-8ab2-fdd82efea0b2" />
  <img width="447" height="702" alt="3 3admindasboard" src="https://github.com/user-attachments/assets/78965ca8-8d16-4b19-93e4-ea584c71f3cb" />
  <img width="1746" height="662" alt="3 4admindasboard" src="https://github.com/user-attachments/assets/ee1ec7a5-51cd-416b-b4eb-e3391e333758" />


---

## ⚡ Getting Started

### Prerequisites

- Python 3.10+
- MongoDB Atlas Account (Cluster with Vector Search configured)
- Google AI API Key

### Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/civicPulse.git
    cd civicPulse
    ```

2.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup**
    Create a `.env` file in the root directory:

    ```env
    GEMINI_API_KEY=your_api_key_here
    Mongo_URL=your_mongodb_connection_string
    ```

4.  **Run the Application**
    ```bash
    streamlit run interface.py
    ```

---






