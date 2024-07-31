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
            'name': 'YYYYY', 
            'age': '23', 
            'gender': 'M',
            'account_type': 'SALARY',
            'pan_number': 'ASDF4967KD',
            'adhaar_number': '345689673947',
    }

files = {
    'bank_statement': open("/Users/yash/BOB-Hackathon-Audit-Compliance/dashboard/uploaded_files/1/bank_statement.pdf", 'rb'),
}

print(data)
print(files)

response = requests.post(url, files=files, data=data)

# Close the files after the request
# files['bank_statement'].close()

if response.status_code == 201:
    print("Data successfully sent to server.")
else:
    print(f"Failed to send data. Status code: {response.status_code}")