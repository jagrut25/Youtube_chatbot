
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# --- Load Environment Variables ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    print("Error: GEMINI_API_KEY not found. Please set it in your .env file.")

# Initialize embeddings once to avoid reloading the model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def process_video_query(video_id, question):
    """Takes a video_id and question and returns the RAG response."""
    try:
        # 1. Fetch Fresh Transcript for Current Video Only
        try:
            transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['en', 'hi'])
            transcript = " ".join([chunk.text for chunk in transcript_list])
        except TranscriptsDisabled:
            return "Transcript is disabled for this video."
        except Exception as e:
            return f"Could not retrieve transcript: {e}. Make sure the video ID is correct and has a transcript."

        # 2. Split Transcript
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.create_documents([transcript])

        # 3. Create NEW Vector Store for ONLY This Video (Critical Change)
        # This ensures no contamination from previous videos
        vector_store = FAISS.from_documents(chunks, embeddings)

        # 4. Retriever - Only retrieves from current video's chunks
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})

        # 5. LLM and Enhanced Prompt Template
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1, api_key=GOOGLE_API_KEY)
        prompt = PromptTemplate(
            template="""
                You are a helpful assistant analyzing a specific YouTube video.
                Answer ONLY based on the provided transcript context from this particular video.
                Do not use any external knowledge or information from other videos.
                If the transcript doesn't contain enough information to answer the question, say "I don't have enough information from this video's transcript to answer that question."
                
                Video Transcript Context:
                {context}
                
                Question: {question}
                
                Answer based solely on the above transcript:
            """,
            input_variables=["context", "question"]
        )

        # 6. RAG Chain
        def format_docs(retrieved_docs):
            return "\n\n".join([doc.page_content for doc in retrieved_docs])

       
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # 7. Invoke Chain and get Response
        response = rag_chain.invoke(question)
        
        # 8. Clean up vector store to free memory (optional but recommended)
        del vector_store
        
        return response

    except Exception as e:
       
        print(f"An unexpected error occurred: {e}")
        return "An error occurred while processing your request. Please check the backend console for details."

# --- API Endpoint Definition ---
@app.route('/ask', methods=['POST'])
def ask_question_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON input'}), 400
        
    video_id = data.get('video_id')
    question = data.get('question')

    if not video_id or not question:
        return jsonify({'error': 'Missing video_id or question'}), 400

    print(f"Processing new request for video_id: {video_id}")
    print(f"Question: '{question}'")
    
    answer = process_video_query(video_id, question)
    
    print(f"Generated answer: '{answer}'")
    
    return jsonify({'answer': answer})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

