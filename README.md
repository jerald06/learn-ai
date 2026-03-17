# AI Chatbot UI

A modern, responsive web interface for interacting with your AI model.

## Features

- Clean, modern chat interface with gradient design
- Real-time typing indicators
- Responsive design for mobile and desktop
- Smooth animations and transitions
- Auto-resizing text input
- Message timestamps
- Connection status indicator

## Setup Instructions

### Prerequisites

1. Make sure you have Ollama installed and running with the `llama3` model
2. Ensure your vector database is created by running `python ingest.py`

### Running the Application

1. **Start the FastAPI backend:**

   ```bash
   cd e:\AI\base-model-ai
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```
2. **Open the chat interface:**

   - Open `e:\AI\base-model-ai\base-model-ui\index.html` in your web browser
   - Or use a simple HTTP server:

     ```bash
     cd e:\AI\base-model-ai\base-model-ui
     python -m http.server 3000
     ```

     Then visit `http://localhost:3000`

### API Endpoints

- `GET /ask?q=your_question` - Get answer via query parameter
- `POST /ask` - Send question in JSON body:
  ```json
  {
    "question": "your question here"
  }
  ```

## File Structure

```
base-model-ui/
├── index.html      # Main HTML structure
├── styles.css      # CSS styling and animations
├── script.js       # JavaScript functionality
└── README.md       # This file
```

## Troubleshooting

1. **CORS Issues**: The FastAPI server is configured to allow all origins for development
2. **Connection Errors**: Make sure Ollama is running on `http://localhost:11434`
3. **No Responses**: Check that your vector database exists in the `./db` directory

## Customization

- Modify the gradient colors in `styles.css` to change the theme
- Update the API URL in `script.js` if your backend runs on a different port
- Add new features to the JavaScript class for enhanced functionality
