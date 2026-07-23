# 🔍 Multi-Agent AI Research System

A **Multi-Agent AI Research System** built with **LangChain**, **Mistral AI**, **Tavily Search**, **BeautifulSoup**, and **Streamlit**.

The system uses multiple AI agents to automatically search the web, extract relevant information, generate a detailed research report, and review the report for quality.

---

## 🚀 Features

- 🔎 AI-powered web search using Tavily
- 🌐 Web page scraping with BeautifulSoup
- 🤖 Multi-agent architecture using LangChain
- ✍️ Automatic research report generation
- 📝 AI-based report review and feedback
- 💻 Interactive Streamlit web interface
- ⚡ Powered by Mistral AI

---

## 🏗️ Project Architecture

```
User
   │
   ▼
Search Agent
   │
   ▼
Reader Agent
   │
   ▼
Writer Agent
   │
   ▼
Critic Agent
   │
   ▼
Final Research Report
```

---

## 📁 Project Structure

```
multi-agent-research-system/
│
├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/MD-ABDULLAH-KHAN/multi-agent-research-system.git
```

---

## 2. Go to the project directory

```bash
cd multi-agent-research-system
```

---

## 3. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate
```

---

### Linux / macOS

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Create the environment file

Create a file named:

```
.env
```

Copy the contents of `.env.example` into it.

Example:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## 6. Get API Keys

### Mistral AI

Create an account and generate an API key:


---

### Tavily Search

Generate a free API key:


---

# ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open automatically in your browser.

If not, visit:

```
http://localhost:8501
```

---

# 🧪 Running from Terminal

You can also execute the research pipeline directly:

```bash
python pipeline.py
```

Enter a research topic when prompted.

Example:

```
Enter a research topic:

Artificial Intelligence in Healthcare
```

---

# 🛠️ Technologies Used

- Python
- LangChain
- Mistral AI
- Tavily Search API
- BeautifulSoup
- Requests
- Streamlit
- Rich
- Pandas

---

# 📦 Requirements

All dependencies are listed in:

```
requirements.txt
```

Install them with:

```bash
pip install -r requirements.txt
```

---

# 🔒 Environment Variables

The application requires:

| Variable | Description |
|----------|-------------|
| MISTRAL_API_KEY | Mistral AI API Key |
| TAVILY_API_KEY | Tavily Search API Key |

---

# 📄 License

This project is intended for educational and research purposes.

---

# 👤 Author

**MD ABDULLAH KHAN**

GitHub:

https://github.com/MD-ABDULLAH-KHAN