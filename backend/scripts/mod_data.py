import os
from dotenv import load_dotenv

from datasets import load_dataset
from huggingface_hub import login

load_dotenv()

# supabase_url = os.getenv("SUPABASE_URL")
# supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
# supabase: Client = create_client(supabase_url, supabase_key)

# embeddings = GoogleGenerativeAIEmbeddings()

login(token=os.getenv("HUGGINGFACE_TOKEN"), write_permission=True)

# load dataset
dataset = load_dataset("Amod/mental_health_counseling_conversations")
# get the training data
data = dataset["train"]
# create a new column that concat the user and agent messages
data = data.map(
    lambda x: {"document": f"<CONTEXT>{x['Context']}</CONTEXT><RESPONSE>{x['Response']}</RESPONSE>"},
    remove_columns=["Context", "Response"],
)
# push modified data to hub
data.push_to_hub("mental_health_concat", private=True)