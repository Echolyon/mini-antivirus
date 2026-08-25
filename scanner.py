import os
from hash_utils import calculate_sha256
from signatures import KNOWN_MALWARE_SIGNATURES
from heuristics import heuristic_scan
from risk_engine import calculate_risk_score, classify_score
from quarantine_manager import quarantine_file
from logger import log_result

RISKY_EXTENSIONS = [
    ".exe", ".com", ".bat", ".cmd", ".vbs", ".js", ".ps1", ".scr"
]

EXCLUDED_DIRS = {"quarantine", "restored", "__pycache__", "archives", "ui", "Output"}


def scan_directory(path):
    results = []

    if not os.path.exists(path):
        return results

    path = os.path.abspath(path)

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            full_path = os.path.join(root, file)

            if not os.path.isfile(full_path):
                continue

            extension = os.path.splitext(file)[1].lower()

            file_info = {
                "path": full_path,
                "name": file,
                "extension": extension,
                "hash": None,
                "status": "CLEAN",
                "risk_score": 0,
                "risk_breakdown": {},
                "heuristic_hits": [],
                "quarantined": False,
                "quarantine_info": None,
                "reason": None
            }

            if extension not in RISKY_EXTENSIONS:
                results.append(file_info)
                log_result(file_info)
                continue

            # HASH
            try:
                file_hash = calculate_sha256(full_path)
                file_info["hash"] = file_hash
            except Exception as e:
                file_info["status"] = "ERROR"
                file_info["reason"] = str(e)
                results.append(file_info)
                log_result(file_info)
                continue

            hash_match = file_hash in KNOWN_MALWARE_SIGNATURES

            # HEURISTIC
            try:
                heuristic_result = heuristic_scan(full_path) or {}
            except:
                heuristic_result = {}

            risk_score, breakdown = calculate_risk_score(
                extension,
                hash_match,
                heuristic_result
            )

            status = classify_score(risk_score)

            file_info["risk_score"] = risk_score
            file_info["risk_breakdown"] = breakdown
            file_info["status"] = status

            # 🔥 OTOMATİK KARANTİNA
            if status == "MALWARE":
                success, q_path = quarantine_file(full_path)
                if success:
                    file_info["quarantined"] = True
                    file_info["quarantine_info"] = q_path
                else:
                    file_info["reason"] = q_path

            results.append(file_info)
            log_result(file_info)

    return results
