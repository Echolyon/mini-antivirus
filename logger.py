from datetime import datetime

LOG_FILE = "scan_report.log"

def log_result(file_info):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    reasons = []
    if file_info.get("hash"):
        if file_info["status"] == "MALWARE":
            reasons.append("HASH_MATCH")
    if file_info.get("risk_score", 0) >= 40:
        reasons.append("HEURISTICS_TRIGGER")
    if file_info.get("quarantined"):
        reasons.append("QUARANTINED")
    
    line = (
        f"[{timestamp}] | "
        f"{file_info['status']} | "
        f"Risk={file_info.get('risk_score', 0)} | "
        f"{file_info['path']} | "
        f"Reasons={','.join(reasons) if reasons else 'NONE'}\n"
    )
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)