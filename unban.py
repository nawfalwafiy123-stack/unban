import smtplib, os, sys, time, json, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- DATABASE ---
DB_FILE = "nopal_data.json"

def load_db():
    if not os.path.exists(DB_FILE):
        data = {
            "users": {}, 
            "accounts": [], 
            "payloads": {
                "1": {"name": "Unban Spam", "sub": "Issue: Spam detection {t}", "body": "Hi, my account {t} was flagged for spam. I was just talking to friends. Please fix."},
                "2": {"name": "Permanen Tinjau", "sub": "Review Appeal {t}", "body": "My account {t} is stuck in review. Please check it manually."},
                "3": {"name": "Permanen Fresh", "sub": "New SIM banned {t}", "body": "I just bought {t} and it is already banned. Please reset."},
                "4": {"name": "Permanen Lumut", "sub": "Old Account Recovery {t}", "body": "Reactivating my old number {t}. It says banned. Help."},
                "5": {"name": "Permanen Batu", "sub": "Final Request {t}", "body": "This is my last appeal for {t}. I need this for work. Please."}
            }
        }
        with open(DB_FILE, "w") as f: json.dump(data, f)
    
    with open(DB_FILE, "r") as f:
        db = json.load(f)
        if "accounts" not in db: db["accounts"] = []
        return db

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

def logo():
    os.system('clear')
    # LOGO ASLI NOPAL (MAINTAINED)
    print(r"""
      ⣠⠂⢀⣠⡴⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢤⣄⠀⠐⣄⠀⠀⠀
    ⠀⢀⣾⠃⢰⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⡆⠸⣧⠀⠀
    ⢀⣾⡇⠀⠘⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠁⠀⢹⣧⠀
    ⢸⣿⠀⠀⠀⢹⣷⣀⣤⣤⣀⣀⣠⣶⠂⠰⣦⡄⢀⣤⣤⣀⣀⣾⠇⠀⠀⠈⣿⡆
    ⣿⣿⠀⠀⠀⠀⠛⠛⢛⣛⣛⣿⣿⣿⣶⣾⣿⣿⣿⣛⣛⠛⠛⠛⠀⠀⠀⠀⣿⣷
    ⣿⣿⣀⣀⠀⠀⢀⣴⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⣀⣠⣿⣿
    ⠛⠻⠿⠿⣿⣿⠟⣫⣶⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣙⠿⣿⣿⠿⠿⠛⠋
    ⠀⠀⠀⠀⠀⣠⣾⠟⣯⣾⠟⣻⣿⣿⣿⣿⣿⣿⡟⠻⣿⣝⠿⣷⣌⠀⠀⠀⠀⠀
    ⠀⠀⢀⣤⡾⠛⠁⢸⣿⠇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⢹⣿⠀⠈⠻⣷⣄⡀⠀⠀
    ⢸⣿⡿⠋⠀⠀⠀⢸⣿⠀⠀⢿⣿⣿⣿⣿⣿⣿⡟⠀⢸⣿⠆⠀⠀⠈⠻⣿⣿⡇
    ⢸⣿⡇⠀⠀⠀⠀⢸⣿⡀⠀⠘⣿⣿⣿⣿⣿⡿⠁⠀⢸⣿⠀⠀⠀⠀⠀⢸⣿⡇
    ⢸⣿⡇⠀⠀⠀⠀⢸⣿⡇⠀⠀⠈⢿⣿⣿⡿⠁⠀⠀⢸⣿⠀⠀⠀⠀⠀⣼⣿⠃
    ⠈⣿⣷⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠈⢻⠟⠁⠀⠀⠀⣼⣿⡇⠀⠀⠀⠀⣿⣿⠀
    ⠀⢿⣿⡄⠀⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⢰⣿⡟⠀
    ⠀⠈⣿⣷⠀⠀⠀⢸⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠃⠀⠀⢀⣿⡿⠁⠀
    ⠀⠀⠈⠻⣧⡀⠀⠀⢻⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡟⠀⠀⢀⣾⠟⠁⠀⠀
    ⠀⠀⠀⠀⠀⠁⠀⠀⠈⢿⣿⡆⠀⠀⠀⠀⠀⠀⣸⣿⡟⠀⠀⠀⠉⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⡄⠀⠀⠀⠀⣰⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠆⠀⠀⠐⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """)
    print("      SC UNBAN | CREATOR : NOPAL")
    print("      TELE : @fvkyzn | WA : 60174667462")
    print("-" * 50)

def admin_panel():
    while True:
        data = load_db()
        logo()
        print("[ MENU ADMIN - CONTROL CENTER ]")
        print("-" * 50)
        print("[1] Manage Email Senders")
        print("[2] Update Text Payload (Spam, Perma, dll)")
        print("[3] Manage Buyer Accounts")
        print("[4] Kembali")
        opt = input("\n[Admin]> ")
        
        if opt == "1":
            logo()
            print("[1] Tambah Email  [2] Hapus Semua  [3] Back")
            sub_opt = input("\n> ")
            if sub_opt == "1":
                em = input("Email: "); pw = input("App Password: ")
                data["accounts"].append({"email": em, "pw": pw}); save_db(data)
            elif sub_opt == "2":
                data["accounts"] = []; save_db(data); print("Cleared!")
        
        elif opt == "2":
            logo()
            print("[ PILIH OPSI YANG INGIN DIUPDATE ]")
            for k, v in data["payloads"].items(): print(f"[{k}] {v['name']}")
            print("[6] Kembali")
            target_pay = input("\n[Admin]> Pilih Nomor: ")
            
            if target_pay in data["payloads"]:
                print(f"\n[*] Update Teks untuk: {data['payloads'][target_pay]['name']}")
                new_sub = input("Subjek Baru (gunakan {t} untuk nomor): ")
                new_body = input("Body Baru (gunakan {t} untuk nomor): ")
                data["payloads"][target_pay]["sub"] = new_sub
                data["payloads"][target_pay]["body"] = new_body
                save_db(data)
                print("\n[+] Text Payload Berhasil Diperbarui!")
                time.sleep(1)
        
        elif opt == "3":
            u = input("User: "); p = input("Pass: ")
            data["users"][u] = p; save_db(data); print("Buyer Created!")
            
        elif opt == "4": break
        time.sleep(0.5)

def unban_engine():
    data = load_db()
    if not data["accounts"]:
        print("\n[!] ERROR: Belum ada email sender!"); time.sleep(2); return
    
    logo()
    print("[ PILIH JENIS SENJATA ]")
    print("-" * 50)
    for k, v in data["payloads"].items(): print(f"[{k}] {v['name']}")
    
    pil = input("\n[?] Pilih Opsi: ")
    if pil not in data["payloads"]: return
    
    target = input("[?] Nomor Target: ")
    print("\n[*] Menembak WhatsApp... JANGAN CANCEL!")
    
    pay = data["payloads"][pil]
    acc = random.choice(data["accounts"])
    
    msg = MIMEMultipart()
    msg['From'] = f"WhatsApp Support <{acc['email']}>"
    msg['Subject'] = pay["sub"].format(t=target)
    msg.attach(MIMEText(pay["body"].format(t=target), 'plain'))

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls(); s.login(acc["email"], acc["pw"])
        s.sendmail(acc["email"], ["support@support.whatsapp.com"], msg.as_string()); s.quit()
        print(f"\n[+] GACOR! {pay['name']} Sukses Terkirim.")
    except Exception as e: print(f"\n[-] Gagal: {e}")
    input("\nEnter lanjut...")

def main():
    logo()
    u = input("[?] User: "); p = input("[?] Pass: ")
    if u == "nopal" and p == "von":
        while True:
            logo()
            print("[1] Fast Unban  [2] Admin Control  [3] Keluar")
            opt = input("\n[Main]> ")
            if opt == "1": unban_engine()
            elif opt == "2": admin_panel()
            elif opt == "3": break
    else:
        db = load_db()
        if db["users"].get(u) == p:
            while True:
                logo()
                print(f"[ USER: {u.upper()} ]")
                print("-" * 50)
                print("[1] Fast Unban  [2] Keluar")
                if input("\n[User]> ") == "1": unban_engine()
                else: break
        else: print("Akses Ditolak!"); time.sleep(2)

if __name__ == "__main__":
    main()
    

