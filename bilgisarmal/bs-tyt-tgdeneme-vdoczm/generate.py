import os
import json

base_dir = os.getcwd()
publisher_prefix = "bilgisarmal"
github_username = "FurkanDundar1"
repo_name = "isler-app-assets"

# GitHub deposundaki bilgisarmal alt klasör yolu
sub_folder = "bilgisarmal/bs-tyt-tgdeneme-vdoczm"

json_data = []
global_id = 1

# Klasördeki MP4 ve alt klasörleri tara
for root, dirs, files in os.walk(base_dir):
    files = sorted(files)
    for file in files:
        if file.lower().endswith('.mp4'):
            # Soru numarasını çek
            q_num = global_id
            try:
                num_part = file.upper().replace('SORU-', '').replace('.MP4', '')
                q_num = int(num_part)
            except ValueError:
                pass

            # Relatif yol hesapla (örn: fen/bs-tyt-fen-tgdeneme-2025-01.mp4)
            rel_path = os.path.relpath(os.path.join(root, file), base_dir).replace('\\', '/')
            folder_name = rel_path.split('/')[0] if '/' in rel_path else "genel"

            item = {
                "id": f"{publisher_prefix}_{global_id}",
                "lesson": folder_name.upper(),
                "questionNo": q_num,
                "videoFileName": file,
                # URL yapısına sub_folder eklendi:
                "videoUrl": f"https://cdn.jsdelivr.net/gh/{github_username}/{repo_name}@main/{sub_folder}/{rel_path}",
                "kazanimCode": f"{folder_name.upper()}-K{q_num}",
                "kazanimlar": [f"{folder_name.capitalize()} Soru {q_num} Video Çözümü"]
            }
            json_data.append(item)
            global_id += 1

output_file = f"{publisher_prefix}_videolar.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print(f"\n[BAŞARILI] Toplam {len(json_data)} video işlendi ve '{output_file}' dosyası oluşturuldu!\n")