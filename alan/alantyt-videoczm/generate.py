import os
import json

base_dir = os.getcwd()
publisher_prefix = "alan"
github_username = "FurkanDundar1"
repo_name = "isler-app-assets"

json_data = []
global_id = 1

# Klasörleri sırayla tara (fen, matematik, sosyal, turkce)
for folder_name in sorted(os.listdir(base_dir)):
    folder_path = os.path.join(base_dir, folder_name)
    
    if os.path.isdir(folder_path):
        files = sorted(os.listdir(folder_path))
        
        for file in files:
            if file.lower().endswith('.mp4'):
                # Soru numarasını dosya adından çek (SORU-1.mp4 -> 1)
                q_num = global_id
                try:
                    num_part = file.upper().replace('SORU-', '').replace('.MP4', '')
                    q_num = int(num_part)
                except ValueError:
                    pass

                item = {
                    "id": f"{publisher_prefix}_{folder_name}_{global_id}",
                    "lesson": folder_name.upper(),
                    "questionNo": q_num,
                    "videoFileName": file,
                    # CDN bağlantısı jsDelivr olarak güncellendi:
                    "videoUrl": f"https://cdn.jsdelivr.net/gh/{github_username}/{repo_name}@main/alantyt/{folder_name}/{file}",
                    "kazanimCode": f"{folder_name.upper()}-K{q_num}",
                    "kazanimlar": [f"{folder_name.capitalize()} Soru {q_num} Video Çözümü"]
                }
                json_data.append(item)
                global_id += 1

output_file = f"{publisher_prefix}_videolar.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print(f"\n[BAŞARILI] Toplam {len(json_data)} video işlendi ve '{output_file}' dosyası oluşturuldu!\n")