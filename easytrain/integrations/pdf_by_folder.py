import os
import requests
import json
import PyPDF2
import time

def add_metadata(text, chunk_number, page_number, file_name, metadata):
    metadata_str = ' '.join(['#' + tag for tag in metadata])
    chunk_metadata = f"#chunk{chunk_number} #page{page_number} #{file_name} {metadata_str}\n"
    return chunk_metadata + text

def send_memory_to_api(payload, api_key):
    url = "https://api.personal.ai/v1/memory"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Memory sent successfully.")
        return True
    else:
        print("Error sending memory. Status code:", response.status_code)
        return False

def process_pdf_file(file_path, chunk_size=64000, metadata=[], api_key=''):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        file_name = os.path.basename(file_path)
        
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            print(f"Processing Page {page_num + 1}:\n{page_text}\n-------------------")

            chunks = [page_text[i:i+chunk_size] for i in range(0, len(page_text), chunk_size)]
            
            for i, chunk in enumerate(chunks):
                chunk_with_metadata = add_metadata(chunk, i + 1, page_num + 1, file_name, metadata)
                payload = {
                    "Text": chunk_with_metadata,
                    "RawFeedText": chunk_with_metadata
                }
                
                success = False
                retries = 0
                while not success and retries < 3:
                    success = send_memory_to_api(payload, api_key)
                    if not success:
                        retries += 1
                        time.sleep(1)
                time.sleep(0.5)

# Scanning directory and subdirectories
folder_path = r'D:\vernoncommunications.ca\VernComm Sharepoint - Documents\04 - Price Lists and Vendor Catalogs'
metadata = ['Large Text File Uploader', 'Chunked by VE7LTX Diagonal Thinking LTD: ve7ltx.cc easytrain.ai Your PDF TEXT: ']
api_key = 'e6fb2eef6a884580a41516f415a7ec72'

for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith('.pdf'):
            file_path = os.path.join(root, file_name)
            print(f"Processing file: {file_path}")
            process_pdf_file(file_path, chunk_size=64000, metadata=metadata, api_key=api_key)
