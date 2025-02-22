import os
from dotenv import load_dotenv

from langchain_community.vectorstores import SupabaseVectorStore
from langchain_community.document_loaders import HuggingFaceDatasetLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from supabase import create_client, Client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# login(token=os.getenv("HUGGINGFACE_TOKEN"), write_permission=False)

# load dataset
loader = HuggingFaceDatasetLoader("menamerai/mental_health_concat", page_content_column="document", use_auth_token=os.getenv("HUGGINGFACE_TOKEN"))
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# upsert data
vector_store = SupabaseVectorStore.from_documents(
    docs,
    embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
    chunk_size=500,
)
