# YouTube Video Chatbot Chrome Extension

A Chrome extension that allows users to ask questions about any YouTube video content using AI-powered analysis of video transcripts.

## 🎯 Features

- **Intelligent Q&A**: Ask any question about a YouTube video's content
- **Real-time Responses**: Get instant AI-powered answers based on video transcripts
- **Multi-language Support**: Works with English and Hindi transcripts
- **Clean Interface**: Simple and intuitive popup interface
- **RAG Technology**: Uses Retrieval-Augmented Generation for accurate responses

## 🏗️ Architecture

The project consists of two main components:

### Frontend (Chrome Extension)
- **Popup Interface**: Clean, user-friendly interface for asking questions
- **Chrome Extension**: Integrates seamlessly with YouTube pages
- **Real-time Communication**: Connects to backend API for processing

### Backend (Flask API)
- **Video Processing**: Extracts and processes YouTube video transcripts
- **AI Integration**: Uses Google's Gemini AI for intelligent responses
- **Vector Search**: Implements FAISS for efficient transcript search
- **RAG Pipeline**: Combines retrieval and generation for accurate answers

## 🚀 Technology Stack

### Frontend
- HTML5, CSS3, JavaScript
- Chrome Extension Manifest V3
- Chrome APIs for tab interaction

### Backend
- **Flask**: Web framework for API endpoints
- **LangChain**: Framework for building AI applications
- **Google Gemini AI**: Large language model for responses
- **FAISS**: Vector database for efficient similarity search
- **HuggingFace Embeddings**: Text embedding generation
- **YouTube Transcript API**: Video transcript extraction

## 📋 Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Gemini API key from Google AI Studio
- Internet connection for API calls

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "youtube chatbot using"
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables
Create a `.env` file in the project root with your API credentials:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Start the Backend Server
```bash
cd backend
python main.py
```
The server will run on `http://localhost:5000`

### 3. Chrome Extension Setup

#### Load the Extension
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked" and select the `frontend` folder
4. The extension will appear in your Chrome toolbar

## 📖 Usage

### Step 1: Navigate to YouTube
Go to any YouTube video page that has captions/transcripts available.

### Step 2: Open the Extension
Click the YouTube Q&A extension icon in your Chrome toolbar.

### Step 3: Ask Questions
- Type your question about the video content in the input field
- Click "Ask Question" to get an AI-powered response
- The response will be based on the video's transcript content

### Example Questions:
- "What is the main topic of this video?"
- "Can you summarize the key points discussed?"
- "What does the speaker say about [specific topic]?"
- "What are the steps mentioned in the tutorial?"

## 🔧 Configuration

### Backend Configuration
The backend can be configured by modifying the following in `main.py`:
- **Port**: Change the port in `app.run(port=5000)`
- **Model**: Switch Gemini models by updating the model name
- **Chunk Size**: Adjust transcript chunking in `RecursiveCharacterTextSplitter`
- **Retrieval**: Modify the number of chunks retrieved with `k` parameter

### Extension Configuration
The extension behavior can be modified in `manifest.json`:
- **Permissions**: Add or remove required permissions
- **Host Permissions**: Modify allowed domains
- **Icons**: Update extension icons and sizes

## 🛠️ API Endpoints

### POST /ask
Ask a question about a YouTube video.

**Request Body:**
```json
{
  "video_id": "youtube_video_id",
  "question": "Your question about the video"
}
```

**Response:**
```json
{
  "answer": "AI-generated response based on video transcript"
}
```

**Error Responses:**
- `400`: Missing video_id or question
- `500`: Server error or processing failure

## 🔍 How It Works

1. **Video Detection**: Extension extracts video ID from current YouTube page
2. **Transcript Retrieval**: Backend fetches video transcript using YouTube API
3. **Text Processing**: Transcript is split into manageable chunks
4. **Embedding Generation**: Text chunks are converted to vector embeddings
5. **Vector Storage**: Embeddings stored in FAISS vector database
6. **Question Processing**: User question is embedded and matched with relevant chunks
7. **AI Response**: Gemini AI generates response based on retrieved context
8. **Result Display**: Answer is displayed in the extension popup

## 🚨 Limitations

- Only works with videos that have available transcripts
- Requires active internet connection
- API rate limits may apply based on your Gemini API usage
- Responses are limited to transcript content only
- Currently supports English and Hindi transcripts

## 🛡️ Privacy & Security

- No user data is stored permanently
- Video transcripts are processed temporarily for each request
- API keys should be kept secure and not shared
- All communication uses HTTPS when possible

## 🆘 Troubleshooting

### Common Issues:

**"Transcript is disabled for this video"**
- The video doesn't have captions/transcripts available
- Try with a different video that has captions

**Backend connection errors**
- Ensure the Flask server is running on port 5000
- Check if the API endpoint URL is correct in the extension

**API key errors**
- Verify your Gemini API key is correct and active
- Check if you have sufficient API quota

**Extension not loading**
- Ensure all files are in the correct directories
- Check Chrome developer console for errors
- Verify manifest.json syntax

