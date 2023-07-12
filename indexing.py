from utils import load_handbook_to_db, get_page_contents

db = load_handbook_to_db(dbname='handbook', glob="*.pdf")

# case 1
query = "How many sick day a year for New York full time employee in Deutsche Bank?"
docs = db.similarity_search(query)
print(get_page_contents(docs))

# case 2
query = "How many days does a full time employee have for COVID-19 Leave?"
docs = db.similarity_search(query)
print(get_page_contents(docs))

# case 3
query = "How can I maintain a healthy work-life balance?"
docs = db.similarity_search(query)
# print(docs[0].page_content)
print(get_page_contents(docs))