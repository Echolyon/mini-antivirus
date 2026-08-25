import os
import shutil
import json
import uuid

QUARANTINE_DIR = "quarantine"
RESTORED_DIR = "restored"

os.makedirs(QUARANTINE_DIR, exist_ok=True)
os.makedirs(RESTORED_DIR, exist_ok=True)


def quarantine_file(file_path):
    try:
        import os
        import shutil
        import json
        import uuid

        os.makedirs("quarantine", exist_ok=True)

        file_name = os.path.basename(file_path)
        unique_id = str(uuid.uuid4())

        quarantined_name = f"{unique_id}_{file_name}.quarantine"
        quarantined_path = os.path.join("quarantine", quarantined_name)

        shutil.move(file_path, quarantined_path)

        metadata = {
            "original_path": file_path,
            "file_name": file_name
        }

        metadata_path = quarantined_path + ".json"

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        return True, quarantined_path

    except Exception as e:
        return False, str(e)


def restore_file(metadata_path):
    try:
        import json
        import os
        import shutil

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        original_path = metadata.get("original_path")
        file_name = metadata.get("file_name")

        if not original_path or not file_name:
            return False, "Metadata bozuk."

        # Gerçek karantina dosyası = JSON isminin .json'suz hali
        quarantined_path = metadata_path.replace(".json", "")

        if not os.path.exists(quarantined_path):
            return False, "Karantina dosyası bulunamadı."

        # Orijinal klasör yoksa restored klasörüne at
        if not os.path.exists(os.path.dirname(original_path)):
            os.makedirs("restored", exist_ok=True)
            original_path = os.path.join("restored", file_name)

        shutil.move(quarantined_path, original_path)

        # JSON'u sil
        os.remove(metadata_path)

        return True, original_path

    except Exception as e:
        return False, str(e)