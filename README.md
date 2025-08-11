# My Multimedia AI Agent (TimeAI Assignment)

Hello! This is my submission for the Ai assignment. I was incredibly excited by the challenge: build a multimedia document agent from scratch. This project was a fantastic learning experience, and I'm proud of what I was able to build in just a few days.

The goal was to create an agent that could intelligently process PDFs, images, and even videos. I decided to take this a step further by building a full **Retrieval-Augmented Generation (RAG)** pipeline for PDFs using Pinecone, which allows for much more efficient and scalable document analysis.

---

##  Core Features

This isn't just a simple Q&A bot. I've built a feature-rich agent with several key capabilities:

*   **True Multimedia Handling:** It can process three different types of media:
    *   **PDFs:** Uses a RAG pipeline. The text is chunked, vectorized, and stored in **Pinecone** for efficient, context-aware retrieval.
    *   **Images:** Analyzed directly by Gemini for visual understanding.
    *   **Videos:** The agent automatically extracts frames at 5-second intervals and analyzes them as a sequence to understand the video's content.
*   **Modular, Industry-Standard Codebase:** I refactored the entire project from a single script into a professional, multi-file structure. This makes the code cleaner, more maintainable, and easier to scale.
*   **Creative AI Personas:** Users can choose an AI "persona" (like *Expert Analyst* or *Creative Brainstormer*) to change the tone and style of the answers.
*   **Flexible Output Formats:** The agent can deliver its response in various formats, including plain text, bullet points, or even structured **JSON**.

---

##  My Architectural Journey

I started with a simple plan but decided to push myself to build something more robust and scalable.

Here’s a breakdown of the final architecture:

1.  **Frontend - `Streamlit`**: I chose Streamlit because it allowed me to build a clean, interactive UI very quickly. The interface is responsible for handling file uploads and displaying the final output.

2.  **Backend Orchestrator - `app.py`**: This is the "brain" of the frontend. It handles the UI logic and calls the appropriate functions from my modules based on user input.

3.  **Processing Modules - `modules/`**: This is where the magic happens. I separated all the core logic into distinct modules for a clean, professional structure.
    *   `utils.py`: Contains the basic file processing functions for PDFs (`process_pdf`) and videos (`process_video`).
    *   `pinecone_utils.py`: This module manages everything related to the RAG pipeline. It connects to Pinecone, creates the index, handles the vector embedding process (using `Sentence-Transformers`), and retrieves the relevant context when a question is asked.
    *   `gemini_utils.py`: This is the final link to the AI. It takes all the context (whether from Pinecone or direct file analysis), combines it with the user's question and creative instructions (persona/format), and gets the final answer from the **Google Gemini 1.5 Flash** model.

![Architecture Diagram](https://i.imgur.com/YOUR_ARCHITECTURE_DIAGRAM_URL.png )
image is also included in repo,

---

##  Getting it Running

I've tried to make it as simple as possible to get this running locally.

### **Prerequisites**
*   Python 3.8+
*   A **Google API Key** with the Gemini API enabled.
*   A **Pinecone API Key** from a free Pinecone account.

### **Architecture Diagram**
[ Streamlit UI ]
     ↓
[ Upload PDF / Image ]
     ↓
[ File Type Detection ]
      ├─ PDF: PyPDF2 → extract text → chunk (1000 chars) → Sentence-Transformers embed → Pinecone upsert
      └─ Image: Pillow (PIL) load → send directly to Gemini Vision (optional: embed for RAG if text detected)
     ↓
[ Pinecone Vector Store ]
     ↓
[ Query Flow ]
    user question → embed (Sentence-Transformers) → Pinecone retrieve → relevant chunks → Gemini Pro Vision → answer
     ↓
[ UI shows answer in Streamlit ]


### **Setup Steps**

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Install all the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(This might take a moment, as it needs to download the sentence-transformer model. )*

3.  **Add your secrets:**
    *   In the project root, create a folder named `.streamlit`.
    *   Inside it, create a file named `secrets.toml`.
    *   Add your API keys like this:
        ```toml
        GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"
        PINECONE_API_KEY = "YOUR_PINECONE_API_KEY_HERE"
        ```

4.  **Run the app!**
    ```bash
    streamlit run app.py
    ```
    Your browser should open with the application running. The first time you run it, it will create a new index in your Pinecone account, which is pretty cool to see!

---

##  Challenges & What I Learned

This project was a sprint, and I ran into some interesting challenges that were great learning opportunities:

*   **The Pinecone Namespace Bug:** I spent a good chunk of time debugging a `Namespace not found` error from Pinecone. I learned that you can't delete from a namespace that doesn't exist yet. The solution was to simplify my logic and just use the `upsert` command, which cleverly handles both creating and overwriting data. This was a great lesson in understanding the nuances of an API.
*   **Refactoring for Readability:** Midway through, my `app.py` file was becoming a monster. I made the decision to pause and refactor everything into a modular structure. It felt like a risk with the tight deadline, but it paid off immensely. The final code is so much cleaner and feels like a real application now.
*   **The Power of RAG:** Seeing the RAG pipeline work for the first time was a huge "aha!" moment. Sending a whole document to an LLM is inefficient. Retrieving only the most relevant chunks first and then sending them to the LLM is so much smarter and more scalable. I'm really excited about the potential of this architecture.

Looking for wonderful feedback, Come on lets improve it together.
