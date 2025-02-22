import os

from langchain_community.vectorstores import SupabaseVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from supabase.client import Client, create_client

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vector_store = SupabaseVectorStore(
    embedding=embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
)

async def vector_retrieval(query: str, limit: int = 10, threshold: float = 0.5) -> list:
    print("Query:", query)
    print("Limit:", limit)
    print("Threshold:", threshold)
    try:
        matched_docs = vector_store.similarity_search_with_score(query, k=limit)
        print(matched_docs)
        return [getattr(doc[0], "page_content", "") for doc in matched_docs if doc[1] > threshold]
    except Exception as e:
        print("Error in vector retrieval:", e)
        return []