import time
import psutil
import requests
import platform
import json
import datetime

def add_metadata(snapshot, snapshot_number, metadata, start_time, end_time, elapsed_time):
    metadata_str = ' '.join(['#' + tag for tag in metadata])
    snapshot_metadata = f"Your Personal Computer's System's Log #snapshot{snapshot_number} {metadata_str} #start_time:{start_time} #end_time:{end_time} #elapsed_time:{elapsed_time}\n"
    snapshot_str = ""
    for key, value in snapshot.items():
        snapshot_str += f"#{key}: {value}\n"
    return snapshot_metadata + snapshot_str

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

def system_info_snapshot():
    start_time = datetime.datetime.now().isoformat()
    start_ms = time.time() * 1000  # convert time to milliseconds
    snapshot = {
        'system': platform.system(),
        'system_version': platform.version(),
        'architecture': platform.architecture(),
        'machine_type': platform.machine(),
        'node': platform.node(),
        'cpu_percent': psutil.cpu_percent(),
        'cpu_frequency': psutil.cpu_freq().current,
        'cpu_count': psutil.cpu_count(logical=True),
        'virtual_memory': psutil.virtual_memory().percent,
        'swap_memory': psutil.swap_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'disk_partitions': str(psutil.disk_partitions()),
        'network_stats': str(psutil.net_io_counters(pernic=True)),
    }
    end_time = datetime.datetime.now().isoformat()
    end_ms = time.time() * 1000  # convert time to milliseconds
    elapsed_time = end_ms - start_ms  # get elapsed time in milliseconds
    return snapshot, start_time, end_time, elapsed_time

api_key = 'e6fb2eef6a884580a41516f415a7ec72'
metadata = ['System Info Snapshot']
snapshot_number = 0
chunk_size = 64000

while True:
    snapshot, start_time, end_time, elapsed_time = system_info_snapshot()
    snapshot_str = add_metadata(snapshot, snapshot_number, metadata, start_time, end_time, elapsed_time)
    chunks = [snapshot_str[i:i+chunk_size] for i in range(0, len(snapshot_str), chunk_size)]
    for i, chunk in enumerate(chunks):
        payload = {
            "Text": chunk,
            "RawFeedText": chunk
        }
        success = False
        retries = 0
        while not success and retries < 3:
            success = send_memory_to_api(payload, api_key)
            if not success:
                retries += 1
                time.sleep(1)
        time.sleep(0.5)
    snapshot_number += 1
    time.sleep(10)
