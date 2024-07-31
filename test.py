
import requests

url = 'http://127.0.0.1:8000/bank_accounts/'

# data = {
#             'name': "YYYYY",
#             'age': "23",
#             'gender': "M",
#             'account_type': "SALARY",
#             'pan_number': "ASDF4567KO",
#             'adhaar_number': "345689671247",
#         }

data = {
    'name': 'aljbvawo',
    'age': 34,  # Changed to integer
    'gender': 'M',
    'account_type': 'SAVINGS',
    'pan_number': 'SIELGNVWO',
    'adhaar_number': '39846573486',
}

files = {
    'bank_statement': open("/Users/yash/BOB-Hackathon-Audit-Compliance/dashboard/uploaded_files/1/bank_statement.pdf", 'rb'),
}

print(data)
print(files)

response = requests.post(url, data=data, files=files)

# Close the files after the request
files['bank_statement'].close()

if response.status_code == 201:
    print("Data successfully sent to server.")
else:
    print(f"Failed to send data. Status code: {response.status_code}")
    print(f"Response content: {response.content}")
