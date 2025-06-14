import streamlit as st
from cohere import ClientV2

# Initialize Cohere Client using secrets
client = ClientV2(api_key=st.secrets["COHERE_API_KEY"])

# Simulated web search results
def search_web(query):
    return [
        {"source": "Wikipedia", "snippet": "Perplexity AI is a conversational AI-powered search engine."},
        {"source": "Cohere Blog", "snippet": "It merges LLM capabilities with search to provide cited answers."},
        {"source": "Arxiv", "snippet": "LLM-powered search engines use contextual understanding to answer user queries."}
    ]

# Construct chat messages format
def generate_messages(question, sources):
    context = "\n".join([f"{s['source']}: {s['snippet']}" for s in sources])
    system_message = {
        "role": "SYSTEM",
        "message": "You are a helpful assistant. Use the following sources to answer the question and include citations."
    }
    user_message = {
        "role": "USER",
        "message": f"Sources:\n{context}\n\nQuestion: {question}"
    }
    return [system_message, user_message]

# Streamlit UI
st.set_page_config(page_title="Perplexity AI Prototype (Cohere v2)")
st.title("Perplexity AI Prototype (Cohere v2)")

# Chat history memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
question = st.text_input("🔍 Ask your question")

if question:
    with st.spinner("Searching and generating answer..."):
        sources = search_web(question)
        messages = generate_messages(question, sources)

        response = client.chat(
            model="command-a-03-2025",
            messages=messages,
            temperature=0.3,
        )

        answer = response.text.strip()

        st.markdown("### ✅ Answer:")
        st.write(answer)

        st.markdown("### 📚 Sources:")
        for s in sources:
            st.markdown(f"- **{s['source']}**: {s['snippet']}")

        # Save to chat history
        st.session_state.chat_history.append({"q": question, "a": answer})

# Display previous questions
if st.session_state.chat_history:
    st.markdown("### 💬 Previous Questions:")
    for i, chat in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
        st.markdown(f"**Q{i}**: {chat['q']}  \n**A{i}**: {chat['a']}")
