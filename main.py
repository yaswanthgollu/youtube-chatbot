import os
from dotenv import load_dotenv

from youtube import get_transcript_from_url
from vectorstore import create_vectorstore
from rag import build_rag_chain

# Load API key
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


def main():
    video_url = input("Enter YouTube URL: ")

    # Step 1: Get transcript
    transcript = get_transcript_from_url(video_url)

    if not transcript:
        return

    # Step 2: Create vector store
    vector_store = create_vectorstore(transcript)

    # Step 3: Build RAG chain
    rag_chain = build_rag_chain(vector_store)

    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = rag_chain.invoke(question)
        print("\nAnswer:\n", answer)


if __name__ == "__main__":
    main()