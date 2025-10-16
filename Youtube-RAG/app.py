import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import os
import google.generativeai as genai
import chromadb

session_state = st.session_state
if 'doc_chunk' not in st.session_state:
    st.session_state.doc_chunk = None

def get_youtube_transcript(video_url):
    video_id = video_url.split("v=")[-1].split("&")[0]
    try:
        ytt_api = YouTubeTranscriptApi()
        result = ytt_api.fetch(video_id)
    
        output = ""
        for snippet in result:
            output += snippet.text
        return output
    
    except Exception as e:
        return f"Could not get transcript: {e}"
    
def chunk_text(text,chunk_size=300):
    words=text.split()
    return ["".join(words[i:i+chunk_size]) for i in range(0,len(words),chunk_size)]

def extract_text_and_store_chunk_in_document(url):
    content = get_youtube_transcript(url)
    chunks = chunk_text(content)
    chroma_client=chromadb.Client()
    if(collection_exists(chroma_client,"my_docs")):
        chroma_client.delete_collection("my_docs")
    collection=chroma_client.create_collection("my_docs")
    for i,chunk in enumerate(chunks):
        collection.add(documents=[chunk],ids=[str(i)])
    return collection

def collection_exists(chroma_client,name):
    try:
        chroma_client.get_collection(name)
        return True
    except chromadb.errors.NotFoundError:
        return False

def rag_query(user_query):
    #genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    collection = st.session_state.doc_chunk
    results = collection.query(query_texts=[user_query],n_results=5)
    retrieved_text = "".join(results["documents"][0])
    prompt = f"""You are an assistant with access to external knowledge.
                 Use the context below to answer the question.
        context:
        {retrieved_text}
        Question:
        {user_query}
        """
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text

st.title("🎥 YouTube Video Q&A (RAG App)")

youtube_url = st.text_input("Enter YouTube video URL:")

if st.button("Process Video"):
    with st.spinner("Fetching transcript and building index..."):
        doc_chunk = extract_text_and_store_chunk_in_document(youtube_url)
        if doc_chunk:
            st.session_state['doc_chunk'] = doc_chunk
            st.success("Document chunking processed successfully!")
        else:
            st.error("Failed to chunk document. Check the URL.")

user_question = st.text_input("Ask a question about the video:")

if user_question:
    with st.spinner("Answering..."):
        answer = rag_query(user_question)
        st.write("**Answer:**", answer)

    

