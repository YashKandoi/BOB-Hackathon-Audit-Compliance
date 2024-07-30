import requests

account_holder_adhaar_number = "123412341234"
account_type = "SAVINGS"

print("Getting Response...")

response = requests.get("http://127.0.0.1:8000/bank_accounts/" + account_holder_adhaar_number + "/" + account_type + "/")

# Parse the JSON response
account_data = response.json()

# Extract the bank_statement and other_documents paths
bank_statement_path = account_data.get("bank_statement")
other_documents_path = account_data.get("other_documents")

print("Bank Statement Path:", bank_statement_path)
print("Other Documents Path:", other_documents_path)
