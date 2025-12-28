# JARVIS Personal AI Assistant 🤖

A smart, modular AI assistant powered by Google Gemini, featuring a Streamlit UI, persistent memory, and role-based personas.

## 🌟 Features

*   **Role-Based Assistance**: Switch between Tutor, Coder, and Mentor roles.
*   **Persistent Memory**: Remembers your conversation across sessions (stored in `memory.json`).
*   **Google Gemini Integration**: Uses the latest Gemini 2.5 Flash model for fast and accurate responses.
*   **Streamlit UI**: Clean and responsive chat interface.
*   **Modular Design**: OOP architecture for easy maintenance and extensibility.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd jarvis_assistant
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  **Get a Google Gemini API Key**:
    *   Visit [Google AI Studio](https://aistudio.google.com/) to create an API key.

2.  **Set up environment variables**:
    *   Create a `.env` file in the project root.
    *   Add your API key:
        ```env
        GENAI_API_KEY=your_api_key_here
        ```

## 🚀 Running the App

Run the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

## 📁 Project Structure

*   `app.py`: Main entry point for the Streamlit UI.
*   `jarvis/`: Core logic modules.
    *   `assistant.py`: Orchestrates the interaction.
    *   `gemini_engine.py`: Handles communication with Gemini API.
    *   `memory.py`: Manages conversation history.
    *   `prompt_controller.py`: Constructs prompts with system and role contexts.
*   `config/`: Configuration files.
*   `memory.json`: JSON file where conversation history is stored (created automatically).

## 🛡️ Requirements

*   Python 3.10+
*   See `requirements.txt` for full list of dependencies.
