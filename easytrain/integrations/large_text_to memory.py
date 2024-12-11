import requests
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

def process_text_file(file_path, chunk_size=64000, metadata=[], api_key=''):
    with open(file_path, 'r') as file:
        content = file.read()
        num_chunks = (len(content) + chunk_size - 1) // chunk_size
        file_name = file_path.split('/')[-1]
        
        for i in range(num_chunks):
            start_index = i * chunk_size
            end_index = start_index + chunk_size
            chunk = content[start_index:end_index]
            
            chunk_with_metadata = add_metadata(chunk, i + 1, i + 1, file_name, metadata)
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
            time.sleep(0.5)  # Delay for 0.5 seconds after each memory is sent

# Example usage
text_file_path = 'example.txt'
metadata = ['Large Text File Uploader', 'Chunked by VE7LTX Diagonal Thinking LTD: ve7ltx.cc easytrain.ai Your TEXT: ']
api_key = 'e6fb2eef6a884580a41516f415a7ec72'
process_text_file(text_file_path, chunk_size=64000, metadata=metadata, api_key=api_key)
