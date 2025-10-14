# 📺 YouTube-RAG

YouTube-RAG is a simple Retrieval-Augmented Generation (RAG) tool that extracts transcripts from YouTube videos and answers user questions in real-time by searching the extracted content.

---

## 🚀 Features

- Extracts transcripts from any public YouTube video
- Allows users to ask questions based on the video content
- Uses Google Gemini LLM for generating accurate, contextual answers
- Fast and interactive web interface with Streamlit

---

## 🧰 Technologies Used

- **Python**
- **Chroma Client**
- **Google Gemini LLM**
- **Streamlit**

---

## 📦 Installation

Follow these steps to set up and run the project locally:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Youtube-RAG.git
cd Youtube-RAG

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key
# Open the 'app.py' file and replace the placeholder with your Gemini API key

# 5. Run the application
streamlit run app.py
