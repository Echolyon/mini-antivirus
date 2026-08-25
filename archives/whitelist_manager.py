import json
import os

WHITELIST_FILE = "whitelist.json"
CLEAN_THRESHOLD = 3

def _load():
    if not os.path.exists(WHITELIST_FILE):
        return {}
    with open (WHITELIST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def _save(data):
    with open(WHITELIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
def is_whitelisted(file_hash: str) -> bool:
    data = _load()
    return file_hash in data and data[file_hash]["whitelisted"] is True

def record_clean(file_hash: str):
    data = _load()
    
    if file_hash not in data:
        data[file_hash] = {
            "clean_count": 1,
            "whitelisted": False
        }
    else:
        data[file_hash]["clean_count"] += 1
        
        if data[file_hash]["clean_count"] >= CLEAN_THRESHOLD:
            data[file_hash]["whitelisted"] = True
    
    _save(data)
    
def add_to_whitelist(file_hash: str):
    data = _load()
    data[file_hash] = {
        "clean_count": CLEAN_THRESHOLD,
        "whitelisted": True
    }
    
    _save(data)