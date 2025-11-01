# [PROJECT NAME, e.g., Aegis AI Coach]

**Team:** [Your Team Name]
**Mission:** To build an AI chatbot that generates hyper-personalized, safe, and effective training programs by understanding a user's goals, biometrics, and injury history.

This README is your guide. It contains the project goals and a file-by-file plan.

---

## 🎯 1. Core Features (The "What")

* **User Onboarding:** Collect user stats (age, weight, goal), `Injury History`, and `Favorite Exercises`.
* **AI-Generated Plans:** Use RAG (Retrieval-Augmented Generation) to create detailed plans.
* **Dynamic Risk Meters:** A visual module that scores an exercise's risk/effectiveness based on the user's profile.
* **Dual-Mode Chat:** A "Quick Tip" mode and an "In-Depth Plan" mode.

---

## 🛠️ 2. Tech Stack (The "Tools")

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React | Modern, fast UI for our webpage. |
| **Backend** | FastAPI (Python) | High-speed API to serve AI logic. |
| **AI Engine** | OpenAI API + LangChain | The "brain" (LLM) and "plumbing" (RAG). |
| **Database** | MongoDB / Firebase | To store user profiles & health data. |
| **Deployment**| Netlify & Render | For fast, scalable deployment. |

---

## 🗺️ 3. File Blueprint (The "Action Plan")

This is the task list for every file in our project.

### `backend/`

* **`requirements.txt`**
    * **Task:** List all Python libraries. Start by adding `fastapi`, `uvicorn`, `langchain`, `openai`, `python-dotenv`, and `faiss-cpu`.

* **`data/expert_knowledge.txt`**
    * **Task:** This is our AI's "expert brain." Write 1-2 paragraph "facts" here.
    * **Example:** "Fact 1: For users with 'lower back pain', barbell deadlifts and high-impact running are high-risk. Recommend goblet squats, bird-dogs, and swimming instead."
    * **Example:** "Fact 2: A 'strength' goal requires 3-5 sets of 4-6 reps with heavy weight. A 'hypertrophy' goal is 3-4 sets of 8-12 reps."

* **`app/main.py`**
    * **Task:** This is our main server.
    * 1.  Import `FastAPI` and `uvicorn`.
    * 2.  Set up **CORS Middleware** so our React frontend can talk to this server.
    * 3.  Import the functions from `ai_engine.py`.
    * 4.  Define the API endpoints (see "API Design" below). The main one will be `POST /api/chat`.

* **`app/schemas.py`**
    * **Task:** Define our Pydantic (data validation) models.
    * 1.  Create `class UserQuery(BaseModel)`: It should have fields like `text: str`, `user_id: str`, `mode: str`.
    * 2.  Create `class AIResponse(BaseModel)`: It should have `response_text: str`, `risk_scores: list`, `youtube_links: list`.

* **`app/ai_engine.py`**
    * **Task:** This is the "brain."
    * 1.  Create a function `get_ai_response(query: UserQuery)`.
    * 2.  This function will:
        * Load the `OPENAI_API_KEY` from a `.env` file (DO NOT hard-code it).
        * Load `data/expert_knowledge.txt` using a `TextLoader`.
        * Create a FAISS vector store from that knowledge (this is the RAG part).
        * Create a `PromptTemplate` for the AI.
        * Use LangChain to combine the prompt, the vector store (retriever), and the OpenAI LLM.
        * Return the AI's final answer.

* **`app/risk_module.py`**
    * **Task:** Create a simple helper function.
    * 1.  Define `def calculate_risk(exercise: str, user_injury: str)`.
    * 2.  For the hackathon, this can be a simple `if-elif-else` block.
    * **Example:** `if 'deadlift' in exercise.lower() and 'back' in user_injury.lower(): return {'risk': 8, 'effectiveness': 9}`.

### `frontend/`

* **`package.json`**
    * **Task:** Add our frontend libraries. Run `npm install axios` to add it.

* **`public/index.html`**
    * **Task:** Change the `<title>Aegis AI Coach</title>` to our project name.

* **`src/index.js`**
    * **Task:** No changes needed. This just boots up React.

* **`src/App.jsx`**
    * **Task:** This is the main app component.
    * 1.  It will hold the main state for the chat history: `const [messages, setMessages] = useState([]);`
    * 2.  It will render the `ChatWindow.jsx` component.
    * 3.  It will contain the `handleSubmit` function. This function will:
        * Take the user's new message.
        * Add the user's message to the `messages` state.
        * Use `axios.post("http://127.0.0.1:8000/api/chat", ...)` to send the message to the FastAPI backend.
        * Get the AI's response and add *that* to the `messages` state.

* **`src/components/ChatWindow.jsx`**
    * **Task:** This is the main UI.
    * 1.  It takes `messages` and `onSend` (our `handleSubmit`) as props.
    * 2.  It will `messages.map((msg) => <ChatMessage ... />)` to display every message.
    * 3.  It will have the text `<input>` bar and the "Send" button at the bottom.

* **`src/components/ChatMessage.jsx`**
    * **Task:** This is a simple display component.
    * 1.  It takes one `message` object as a prop (e.g., `{ text: "Hello", sender: "user" }`).
    * 2.  It will use CSS (`index.css`) to show a gray bubble if `sender === 'user'` and a blue bubble if `sender === 'ai'`.
    * 3.  It will also render any `RiskMeter` components if they are in the message.

* **`src/components/RiskMeter.jsx`**
    * **Task:** This is our new "Innovation" component.
    * 1.  It takes `props` like `label="Risk"` and `score=8`.
    * 2.  It will use CSS to display a simple visual "progress bar" or "meter" that is 8/10 full and colored (e.g., red).

---

## 🔗 4. API Design (The "Contract")

This is how the frontend and backend will talk.

### `POST /api/chat`

* **Frontend Sends (Request Body):**
    ```json
    {
      "text": "Give me a 3-day strength plan.",
      "user_id": "user-123",
      "mode": "in-depth",
      "history": [
        { "sender": "user", "text": "Hi" },
        { "sender": "ai", "text": "Hello!" }
      ]
    }
    ```

* **Backend Responds (Response Body):**
    ```json
    {
      "response_text": "Here is your 3-day plan...\nDay 1: ...",
      "risk_scores": [
        { "exercise": "Deadlift", "risk": 7, "effectiveness": 9 }
      ],
      "youtube_links": [
        { "exercise": "Deadlift", "url": "[https://youtube.com/](https://youtube.com/)..." }
      ]
    }
    ```

---

## 🏃‍♂️ 5. How to Run Locally

### 1. Run the Backend (FastAPI)

```bash
# From the root folder:
cd backend
# Create a virtual environment (optional but recommended)
# python -m venv venv
# venv\Scripts\activate
pip install -r requirements.txt
# Create a .env file and add your OPENAI_API_KEY
uvicorn app.main:app --reload
```bash
### 2. Run the Frontend

# From the root folder, in a *new* terminal:
```bash
cd frontend
npm install
npm start
```bash