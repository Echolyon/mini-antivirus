import re


SUSPICIOUS_KEYWORDS = [
    "invoke-webrequest",
    "downloadstring",
    "iex",
    "invoke-expression",
    "executionpolicy bypass",
    "base64",
    "frombase64string"
]


def heuristic_scan(file_path):
    result = {
        "score": 0,
        "hits": [],
        "critical": False,
        "url": None
    }

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()

        # 🔎 Anahtar kelimeler
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in content:
                result["score"] += 15
                result["hits"].append(keyword)

        # 🌐 URL yakalama
        url_match = re.search(r"http[s]?://[^\s\"']+", content)
        if url_match:
            url = url_match.group(0)
            result["url"] = url
            result["score"] += 20
            result["hits"].append("external_url")

        # ⚠️ Kritik kombinasyonlar
        if "invoke-webrequest" in content and url_match:
            result["score"] += 30
            result["critical"] = True
            result["hits"].append("download_behavior")

        if "base64" in content and ("iex" in content or "invoke-expression" in content):
            result["score"] += 40
            result["critical"] = True
            result["hits"].append("encoded_execution")

    except Exception:
        pass

    return result
