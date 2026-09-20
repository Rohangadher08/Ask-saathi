# agent/rag.py

import json
import os

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# -------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(BASE_DIR, "data")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")


# -------------------------------------------------
# LOAD JSON FILE
# -------------------------------------------------

def load_json(filename):
    """Load JSON data from the data folder."""

    file_path = os.path.join(DATA_DIR, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# -------------------------------------------------
# CREATE DOCUMENTS
# -------------------------------------------------

def create_documents():
    """Convert schemes and policies into LangChain documents."""

    schemes = load_json("schemes.json")
    policies = load_json("policies.json")

    documents = []

    # Government schemes
    for scheme in schemes:

        content = f"""
Government Scheme: {scheme.get("name", "")}

Category: {scheme.get("category", "")}

Target: {scheme.get("target", "")}

Purpose: {scheme.get("purpose", "")}

Benefit: {scheme.get("benefit", "")}

Relevance: {scheme.get("relevance", "")}

Eligibility: {scheme.get("eligibility", "")}

Source: {scheme.get("source", "")}

Keywords: {", ".join(scheme.get("keywords", []))}
"""

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "type": "government_scheme",
                    "name": scheme.get("name", "")
                }
            )
        )

    # Government policies
    for policy in policies:

        content = f"""
Policy: {policy.get("title", "")}

Category: {policy.get("category", "")}

Topic: {policy.get("topic", "")}

Description: {policy.get("description", "")}

Relevance: {policy.get("relevance", "")}

Keywords: {", ".join(policy.get("keywords", []))}

Source: {policy.get("source", "")}
"""

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "type": "policy",
                    "name": policy.get("title", "")
                }
            )
        )

    return documents


# -------------------------------------------------
# CREATE / LOAD VECTOR STORE
# -------------------------------------------------

def get_vectorstore():
    """Create the Chroma vector database."""

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    documents = create_documents()

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )

    return vectorstore


# -------------------------------------------------
# SEARCH RAG KNOWLEDGE
# -------------------------------------------------

def search_knowledge(query, k=3):
    """Search relevant schemes and policies."""

    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    return results


# -------------------------------------------------
# GET RAG CONTEXT
# -------------------------------------------------

def get_rag_context(query, k=3):
    """Return retrieved knowledge as text."""

    results = search_knowledge(query, k)

    if not results:
        return "No relevant information found."

    context = []

    for i, document in enumerate(results, start=1):

        context.append(
            f"""
--- Retrieved Information {i} ---

{document.page_content}
"""
        )

    return "\n".join(context)


# -------------------------------------------------
# TEST RAG
# -------------------------------------------------

if __name__ == "__main__":

    query = input(
        "Ask Vyapar Saathi about schemes or policies: "
    )

    print("\nSearching knowledge base...\n")

    result = get_rag_context(query)

    print(result)