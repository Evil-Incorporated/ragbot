import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
# Check if the API key is set before proceeding
if not os.environ.get("NVIDIA_API_KEY"):
    raise ValueError(
        "❌ NVIDIA_API_KEY is missing! If not already created, create a .env file and add the line \"NVIDIA_API_KEY=<your_api_key>\""
    )

pdf_path = "my_resume.pdf"

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"❌ Could not find a file at: {pdf_path}")

print(f"⏳ Loading and processing '{pdf_path}'...")

print("🔗 Connecting to hosted NVIDIA NIM Cloud endpoints...")

# --- 1. INITIALIZE HOSTED NVIDIA MODELS ---
# By leaving out 'base_url', the SDK defaults to NVIDIA's API Catalog cloud endpoints
embedding_model = NVIDIAEmbeddings(
    model="nvidia/llama-nemotron-embed-1b-v2"
)

llm = ChatNVIDIA(
    model="meta/llama-3.3-70b-instruct",  # Using a larger model since it's hosted in the cloud!
    temperature=0.2,
)

# --- 2. SETUP VECTOR STORE (LOCAL MEMORY) ---
# Load the PDF file
loader = PyPDFLoader(pdf_path)
raw_documents = loader.load()

# Split the text into manageable chunks so the embedding model handles it efficiently
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Characters per chunk
    chunk_overlap=200, # Overlap between chunks to prevent split context
)
docs = text_splitter.split_documents(raw_documents)

print(f"✨ Split PDF into {len(docs)} chunks. Indexing into vector database...")

vectorstore = Chroma.from_documents(documents=docs, embedding=embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 chunks

# --- 3. CONSTRUCT CONVERSATIONAL RAG CHAIN ---
contextual_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a HR recruiter looking to hire a candidate. Answer the user's question using ONLY the "
            "provided context below. If you do not know the answer based on the context, say so.\n\n"
            "Context:\n{context}",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chain mapping (LCEL pipeline)
rag_chain = (
    {
        "context": lambda x: format_docs(retriever.invoke(x["question"])),
        "question": lambda x: x["question"],
        "history": lambda x: x["history"],
    }
    | contextual_prompt
    | llm
    | StrOutputParser()
)

# --- 4. CONVERSATIONAL MEMORY TRACKING ---
session_store = {}


def get_session_history(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]


conversational_rag_chatbot = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# --- 5. TERMINAL USER INTERFACE ---
print("\n✨ Cloud Chatbot with NVIDIA NIM & RAG is ready! (Type 'exit' to quit)")
print("-" * 60)
session_id = "cloud_session_01"

while True:
    user_query = input("\nYou: ")
    if user_query.lower() in ["exit", "quit"]:
        print("Closing assistant connection. Goodbye!")
        break

    if not user_query.strip():
        continue

    print("AI: ", end="", flush=True)

    # Invoke stream natively across the cloud connection
    config = {"configurable": {"session_id": session_id}}
    for chunk in conversational_rag_chatbot.stream(
        {"question": user_query}, config=config
    ):
        print(chunk, end="", flush=True)
    print()

    # --- 5. TERMINAL USER INTERFACE ---
print("\n✨ Cloud Chatbot with NVIDIA NIM & RAG is ready! (Type 'exit' to quit)")
print("-" * 60)
session_id = "cloud_session_01"

while True:
    user_query = input("\nYou: ")
    if user_query.lower() in ["exit", "quit"]:
        print("Closing assistant connection. Goodbye!")
        break

    if not user_query.strip():
        continue

    print("AI: ", end="", flush=True)

    # Invoke stream natively across the cloud connection
    config = {"configurable": {"session_id": session_id}}
    for chunk in conversational_rag_chatbot.stream(
        {"question": user_query}, config=config
    ):
        print(chunk, end="", flush=True)
    print()

