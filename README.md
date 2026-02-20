# AI Chatbot API 🤖

A **Python FastAPI chatbot** that uses **Groq LLM** and **MongoDB** to store conversation history.  
You can ask questions about Python apps, and the bot remembers your chat history per user.

---

## 🚀 Features

- FastAPI backend with **REST API**
- Persistent **MongoDB memory**
- Integration with **Groq LLM** for AI responses
- Swagger UI documentation automatically generated
- Fully environment-variable based (secure API keys)
- Easily deployable to cloud platforms (Render, Railway, VPS)

---

## 🛠 Tech Stack

- **Python 3.10+**
- **FastAPI** – API framework
- **LangChain** – LLM integration
- **Groq** – AI model
- **MongoDB Atlas** – Conversation storage
- **Uvicorn** – ASGI server
- **Pydantic** – Request validation

---

## 📁 Project Structure


```

CHATBOT/
│
├── app.py              # FastAPI main app
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignore venv, .env, cache files
├── README.md           # Project documentation
└── .env                # Environment variables (not pushed)

````

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_uri
````

**Do NOT commit `.env`** (it's in `.gitignore`).

---

## 💻 Install & Run Locally

1. Clone the repo:

```bash
git clone https://github.com/Simon3222/Chatbot.git
cd Chatbot
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
uvicorn app:app --reload --port 5000
```

Open your browser:

```
http://127.0.0.1:5000
```

Swagger docs:

```
http://127.0.0.1:5000/docs
```

---

## 🔗 API Endpoints

### 1️⃣ Health Check

* **GET /**

Response:

```json
{
  "message": "Chatbot API is running 🚀"
}
```

---

### 2️⃣ Chatbot

* **POST /chat**

Request Body:

```json
{
  "user_id": "user123",
  "question": "Who am I?"
}
```

Response:

```json
{
  "user_id": "user123",
  "answer": "Your name is Simon."
}
```

---

## 🧠 Conversation History

* Every message is stored in MongoDB under a `user_id`
* Supports multiple users
* AI uses previous messages as context for better answers

---

## 🔐 Security

* `.env` keeps API keys private
* MongoDB Atlas connection uses TLS/SSL for secure communication

---

## 💡 Deployment Tips

* Use **Render** or **Railway** for easy deployment
* Make sure to set environment variables in deployment settings
* Use **`requirements.txt`** to install dependencies automatically

---

## 📌 Notes

* Port 5000 is recommended if 8000 is blocked
* Stop Uvicorn properly with **CTRL+C** to avoid port lock issues

---

## ⭐ Author

**Simon Mugaka** – [GitHub](https://github.com/Simon3222)



