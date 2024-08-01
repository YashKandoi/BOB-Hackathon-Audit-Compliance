# BOB-Hackathon-Audit-Compliance
Manual methods are prone to errors and inefficiencies. By leveraging generative AI, we aim to revolutionize audit and compliance, making these processes faster and more reliable, and ensuring organizations stay compliant with evolving regulations.

![overview](https://github.com/user-attachments/assets/5dd8329a-6614-498e-8337-2890688b0498)

We bring to you **ComplianceAI**, the all-in-one Compliance and Audit tool of 2024 that brings in GenAI features to make your banking easier. Some remarkable features of our product:

1. Continuously monitors and updates compliance requirements, adapting to new regulations and standards set by the **Reserve Bank of India**.
2. Generate **comprehensive compliance audit reports** with minimal human intervention by mapping them to these latest RBI Guidelines.
3. Checks for **several compliances(AML, KYC**) distributed over **different account types** (Savings, Current, Salary, Fixed Deposit, Recurring Deposit, NRI) and flags them if any **suspicious activity** has been detected.
4. Displays several insights about the different bank accounts and the savings made through the tool.
5. Top-notch **Privacy and Data Security** is maintained by creating different vector stores for each user's bank account and is only visible to the bank in the Azure Portal. This can also be deleted post-generation of audit reports.
6. **Highly Scalable** through Azure Solutions.
7. **Easy Development and Maintainance** of the System since the entire project has been built using Django as the backend framework used by several large organisations.
8. Option to change and edit compliance available on the product for **easy integration into the bank's requirements**.

## RBI Guidelines Updater Page
![rbi_guidelines](https://github.com/user-attachments/assets/de1cf9d3-aec7-4737-8ac7-25436d607535)

## Create Bank Account Page
![create_account](https://github.com/user-attachments/assets/9a875ae4-2fcb-4e8c-9044-79cb99f7e0c9)

## Download Audit Reports Page
![users](https://github.com/user-attachments/assets/f8bdca52-6d20-42e3-8b79-5ffaa36600a1)

## Azure Tools Used
1. Azure Assistants API: For Generating the Audit Reports
2. Azure OpenAI: For LLM prompting and generating responses
3. Azure AI Search: For storing the latest RBI compliance reports.

# Steps to Run

1. Clone the Repository from Github in an IDE from [ComplianceAI](https://github.com/YashKandoi/BOB-Hackathon-Audit-Compliance) or Download the Zip File.

2. Creating a virtual environment
   You can create a virtual env and choose to run you code on that. Open your terminal and do this:
   1. ```python3 -m venv .venv```
   2. ```. .venv/bin/activate```
  
3. Run
   ```pip install -r requirements.txt```
   This will take some time and install all required libraries.

4. Run
    ```rav run server``` to start Django Backend Server.

5. Open another terminal and Run
     ```rav run frontend``` to run the frontend application.

6. Go to the frontend server shown in the terminal and this will start **ComplianceAI**.

--------------------------------------------------------------------------------------
[Demo Video](https://youtu.be/z_S7mBHjZnc?feature=shared) | [Setup Video](https://www.loom.com/share/ec8186f0bb7447b58094fb40f1bd5d87?sid=2aef8a0e-4fbe-4b11-960b-7be4ea34d3d8)
Created with ❤️ by [Yash Kumar Kandoi](https://github.com/YashKandoi) , [Suvid Singhal](https://github.com/Suvid-Singhal) & [Aditya Deshpande](https://github.com/adityadeshpande04)
