import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
import tempfile
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# 1. Page Configuration
st.set_page_config(page_title="PDF Summary & Q&A Assistant", page_icon="📄", layout="wide")
st.title("📄 PDF Summary & Q&A Assistant")
st.write("Upload a PDF file, review its automatic summary, and ask specific questions about its content.")

# Check for API Key
if not os.environ.get("OPENAI_API_KEY"):
    st.error("Please set your `OPENAI_API_KEY` environment variable or add it to your system variables.")
    st.stop()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# Initialize Session State variables so data persists across clicks
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 2. Sidebar - File Upload & Document Info
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_file:
        # Check if we are uploading a NEW file to reset the state
        if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
            st.session_state.current_file = uploaded_file.name
            st.session_state.rag_chain = None
            st.session_state.summary = None
            st.session_state.chat_history = []
        
        if st.session_state.rag_chain is None:
            with st.spinner("Processing PDF (Loading, Chunking, Summarizing)..."):
                try:
                    # Save uploaded file temporarily so PyPDFLoader can read it
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name

                    # Load PDF
                    loader = PyPDFLoader(tmp_file_path)
                    docs = loader.load()
                    
                    # Generate Summary
                    summary_prompt = ChatPromptTemplate.from_template(
                        "Write a comprehensive summary of the following text, highlighting the main points:\n\n{context}"
                    )
                    summary_chain = create_stuff_documents_chain(llm, summary_prompt)
                    st.session_state.summary = summary_chain.invoke({"context": docs})

                    # Setup RAG for Q&A
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                    final_chunks = text_splitter.split_documents(docs)
                    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
                    vector_store = FAISS.from_documents(final_chunks, embeddings)
                    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

                    qa_prompt = ChatPromptTemplate.from_template("""
                    You are an intelligent assistant. Answer the user's question accurately using ONLY the provided context below.
                    If you do not know the answer based on the context, say "I cannot find that information in the document."

                    Context:
                    {context}

                    Question: {input}
                    Answer:""")

                    combine_docs_chain = create_stuff_documents_chain(llm, qa_prompt)
                    st.session_state.rag_chain = create_retrieval_chain(retriever, combine_docs_chain)
                    
                    # Clean up temporary file
                    os.remove(tmp_file_path)
                    st.success("PDF processed successfully!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.stop()

# 3. Main Dashboard Layout Split
if st.session_state.rag_chain is not None:
    col1, col2 = st.columns([1, 1])

    # Left Column: Document Summary Display
    with col1:
        st.subheader("📝 Executive Summary")
        st.info(st.session_state.summary)

    # Right Column: Interactive Chat Interface
    with col2:
        st.subheader("💬 Ask Questions")
        
        # Display existing chat message history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input query
        if user_query := st.chat_input("Ask something about the document..."):
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_query)
            st.session_state.chat_history.append({"role": "user", "content": user_query})

            # Generate RAG response
            with st.chat_message("assistant"):
                with st.spinner("Searching document details..."):
                    response = st.session_state.rag_chain.invoke({"input": user_query})
                    answer = response["answer"]
                    st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
else:
    st.info("👈 Please upload a PDF file in the sidebar to get started.")