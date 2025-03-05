## LangChain: E-Commerce (Flipkart) RAG QnA Chatbot App


### Overview:
- The goal of the chatbot app is to facilitate the customers with the information about the various earphones/headphones available on the platform.
- This app is a demo app created using the LangChain framework and the FAISS vector store.
- App is based on the downloaded data about some of the earphones/headphones products on E-Commerce platform Flipkart.
- This app has single version implemented with memory and streamed chat.


### Dataset:
- Input Data: CSV file provided in the 'data' folder
- Vector Store: Inside 'faiss_vector_store' folder.
- Chat History: SQLite DB file 'ecom_chats.db'


### Implementation Process:
- Follow the Jupyter Notebook to see the implementation process in detail.


### App:
- Inside the 'app' folder.
- Install the necessary packages using 'requirements.txt'
- Set the GROQ_API_KEY in the '.env' file to run the app.


### Tech Stack:
- LangChain
- Ollama
- FAISS
- Groq API
- Streamlit
- Pandas
