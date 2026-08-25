import hashlib

def calculate_sha256(file_path):
    """
    Verilen dosyanın SHA-256 hash değerini hesaplar.
    """
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                sha256.update(chunk)

        return sha256.hexdigest()

    except (PermissionError, FileNotFoundError):
        return None