from quarantine_manager import restore_file

quarantined_file = "quarantine/malware.ps1.1770660157.quarantine"

success, result = restore_file(quarantined_file)

if success:
    print("[+] Restore edildi:", result)
else:
    print("[-] Restore başarısız:", result)
