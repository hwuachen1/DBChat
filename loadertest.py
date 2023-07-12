from utils import *

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=os.path.join('db', 'handbook'), embedding_function=embedding_function)

# case 1
query = "How many sick day a year for New York full time employee in Deutsche Bank?"
docs = db.similarity_search(query)
print(get_page_contents(docs))
