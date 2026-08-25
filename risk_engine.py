from urllib.parse import urlparse

TRUSTED_DOMAINS = [
    "microsoft.com",
    "google.com",
    "github.com",
    "youtube.com"
]


def is_trusted_domain(url: str) -> bool:
    try:
        domain = urlparse(url).netloc.lower()
        return any(domain.endswith(td) for td in TRUSTED_DOMAINS)
    except:
        return False


def calculate_risk_score(extension, hash_match, heuristic_result):
    score = 0
    breakdown = {}

    # 📁 Extension risk
    if extension in [".exe", ".com", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".scr"]:
        score += 10
        breakdown["extension"] = 10

    # 🧬 Hash match
    if hash_match:
        score += 100
        breakdown["hash_match"] = 100

    # 🔍 Heuristic
    if heuristic_result:
        h_score = heuristic_result.get("score", 0)
        if h_score:
            score += h_score
            breakdown["heuristic"] = h_score

        url = heuristic_result.get("url")
        if url:
            if is_trusted_domain(url):
                score -= 30
                breakdown["trusted_domain_bonus"] = -30
            else:
                score += 30
                breakdown["untrusted_domain"] = 30

        if heuristic_result.get("critical"):
            score += 40
            breakdown["critical_behavior"] = 40

    return max(score, 0), breakdown


def classify_score(score):
    if score >= 90:
        return "MALWARE"
    elif score >= 50:
        return "SUSPICIOUS"
    else:
        return "CLEAN"
