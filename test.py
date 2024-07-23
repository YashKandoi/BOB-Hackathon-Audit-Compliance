final_response = """
assistant: ### KYC.txt

#### Current Account
**Requirement: Proof of Identity**  
Description: Submit a valid Aadhaar card or PAN card.  
Citation: RBI Guidelines 2024, Section 16 

**Requirement: Proof of Address**  
Description: Submit a recent utility bill or rent agreement.  
Citation: RBI Guidelines 2024, Section 16 

#### Savings Account
**Requirement: Proof of Identity**  
Description: Submit a valid Aadhaar card or PAN card.  
Citation: RBI Guidelines 2024, Section 16 

**Requirement: Proof of Address**  
Description: Submit a recent utility bill or rent agreement.  
Citation: RBI Guidelines 2024, Section 16 

#### Salary Account
**Requirement: Proof of Identity**  
Description: Submit a valid Aadhaar card or PAN card.  
Citation: RBI Guidelines 2024, Section 16 

**Requirement: Proof of Address**  
Description: Submit a recent utility bill or rent agreement.  
Citation: RBI Guidelines 2024, Section 16 

#### Fixed Deposit Account
**Requirement: Proof of Identity**  
Description: Submit a valid Aadhaar card or PAN card.  
Citation: RBI Guidelines 2024, Section 16 

**Requirement: Proof of Address**  
Description: Submit a recent utility bill or rent agreement.  
Citation: RBI Guidelines 2024, Section 16 

#### Recurring Deposit Account
**Requirement: Proof of Identity**  
Description: Submit a valid Aadhaar card or PAN card.  
Citation: RBI Guidelines 2024, Section 16 

**Requirement: Proof of Address**  
Description: Submit a recent utility bill or rent agreement.  
Citation: RBI Guidelines 2024, Section 16 

#### NRI Accounts
**Requirement: Proof of Identity**  
Description: Submit a valid passport and visa.  
Citation: RBI Guidelines 2024, Section 44 

**Requirement: Proof of Address**  
Description: Submit proof of address in the home country and a local address declaration within 30 days.  
Citation: RBI Guidelines 2024, Section 44 

---

### AML.txt

#### Current Account
**Requirement: Transaction Monitoring**  
Description: Monitor transactions exceeding INR 10 lakhs.  
Citation: RBI Guidelines 2024, Section 5A 

**Requirement: Suspicious Activity Reporting**  
Description: Report any suspicious activities to the relevant authorities.  
Citation: RBI Guidelines 2024, Section 5A 

#### Savings Account
**Requirement: Transaction Monitoring**  
Description: Monitor transactions exceeding INR 10 lakhs.  
Citation: RBI Guidelines 2024, Section 5A 

**Requirement: Suspicious Activity Reporting**  
Description: Report any suspicious activities to the relevant authorities.  
Citation: RBI Guidelines 2024, Section 5A 

#### Salary Account
**Requirement: Transaction Monitoring**  
Description: Monitor transactions exceeding INR 10 lakhs.  
Citation: RBI Guidelines 2024, Section 5A 

**Requirement: Suspicious Activity Reporting**  
Description: Report any suspicious activities to the relevant authorities.  
Citation: RBI Guidelines 2024, Section 5A 

#### Fixed Deposit Account
**Requirement: Transaction Monitoring**  
Description: Monitor transactions exceeding INR 10 lakhs.  
Citation: RBI Guidelines 2024, Section 5A 

**Requirement: Suspicious Activity Reporting**  
Description: Report any suspicious activities to the relevant authorities.  
Citation: RBI Guidelines 2024, Section 5A 

#### Recurring Deposit Account
**Requirement: Transaction Monitoring**  
Description: Monitor transactions exceeding INR 10 lakhs.  
Citation: RBI Guidelines 2024, Section 5A 

**Requirement: Suspicious Activity Reporting**  
Description: Report any suspicious activities to the relevant authorities.  
Citation: RBI Guidelines 2024, Section 5A 

#### NRI Accounts
**Requirement: Enhanced Due Diligence**  
Description: Conduct enhanced due diligence for high-risk accounts.  
Citation: RBI Guidelines 2024, Section 5A 

**Requirement: Periodic Review**  
Description: Perform periodic reviews of the account activities.  
Citation: RBI Guidelines 2024, Section 5A 
"""

def save_to_file(final_response):
        # Split the response by the section headers
    sections = final_response.split('---')

    # Extract KYC section
    kyc_section = sections[0].split('### KYC.txt\n')[1]

    # Extract AML section
    aml_section = sections[1].split('### AML.txt\n')[1]

    # Write KYC section to a file
    with open('complicanceAI/regulations_files/KYC.txt', 'w') as kyc_file:
        kyc_file.write('KYC Rules: \n' +kyc_section)

    # Write AML section to a file
    with open('complicanceAI/regulations_files/AML.txt', 'w') as aml_file:
        aml_file.write('AML Rules: \n' + aml_section)

    print("Files created successfully!")

save_to_file(final_response)
