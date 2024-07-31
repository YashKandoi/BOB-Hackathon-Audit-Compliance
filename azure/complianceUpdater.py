import sys
import os

# Add the directory containing complianceUpdater.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from RBI_DataFetcher import main as RBI_main
from complianceAssitant import main as compliance_main

def main():
    RBI_main()
    compliance_main()

# if __name__ == '__main__':
#     main()