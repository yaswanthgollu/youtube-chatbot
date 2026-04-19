from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# format docs
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(vector_store):
    # Retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2
    )

    # Prompt
    prompt = PromptTemplate(
        template="""
You are a helpful assistant.
Answer ONLY from the provided transcript context.
If the context is insufficient, just say you don't know.

{context}

Question: {question}
""",
        input_variables=["context", "question"]
    )

    # Parser
    parser = StrOutputParser()

    # Chain
    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    main_chain = parallel_chain | prompt | llm | parser

    return main_chain