import os

for file in os.listdir('azure/RBI_Guidelines_Documents'):
        os.remove(f'azure/RBI_Guidelines_Documents/{file}')