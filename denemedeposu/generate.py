import os
import json
import urllib.parse  # URL kodlama kütüphanesi eklendi
import pandas as pd

base_dir = os.getcwd()
publisher_prefix = "denemedeposu"  # Yayın adı (acil, alan, bilgisarmal, denemedeposu)
github_username = "FurkanDundar1"
repo_name = "isler-app-assets"

json_data = []
pdf_files = []
answer_keys = {}

# 1. ADIM: Klasördeki PDF ve Excel Dosyalarını Tespit Et
for root, dirs, files in os.walk(base_dir):
    for file in files:
        rel_path = os.path.relpath(os.path.join(root, file), base_dir).replace('\\', '/')
        encoded_pdf_path = urllib.parse.quote(rel_path)  # PDF URL'leri için kodlama yapıldı
        
        # PDF Kitapçıklarını Topla
        if file.lower().endswith('.pdf'):
            pdf_files.append({
                "fileName": file,
                "pdfUrl": f"https://raw.githubusercontent.com/{github_username}/{repo_name}/main/{publisher_prefix}/{encoded_pdf_path}"
            })
            
        # Excel Cevap Anahtarı / Kazanım Tablolarını Oku
        elif file.lower().endswith('.xlsx') or file.lower().endswith('.xls'):
            excel_path = os.path.join(root, file)
            try:
                # Excel'i Oku (İlk sayfayı varsayılan olarak alır)
                df = pd.read_excel(excel_path)
                # Örnek kolon isimleri aranır (Soru, Cevap, Kazanım)
                for index, row in df.iterrows():
                    q_no = row.get('Soru No', row.get('Soru', index + 1))
                    ans = row.get('Cevap', row.get('Cevap Anahtarı', ''))
                    kazanim = row.get('Kazanım', row.get('Konu', ''))
                    
                    if pd.notna(q_no):
                        answer_keys[str(int(q_no) if isinstance(q_no, (int, float)) else q_no)] = {
                            "answer": str(ans).strip() if pd.notna(ans) else "",
                            "kazanim": str(kazanim).strip() if pd.notna(kazanim) else ""
                        }
            except Exception as e:
                print(f"[UYARI] Excel okunamadı ({file}): {e}")

# 2. ADIM: Video Dosyalarını Tara ve Tüm Veriyi Birleştir
global_id = 1
for root, dirs, files in os.walk(base_dir):
    files = sorted(files)
    for file in files:
        if file.lower().endswith('.mp4'):
            q_num = global_id
            try:
                num_part = file.upper().replace('SORU-', '').replace('.MP4', '')
                q_num = int(num_part)
            except ValueError:
                pass

            rel_path = os.path.relpath(os.path.join(root, file), base_dir).replace('\\', '/')
            encoded_video_path = urllib.parse.quote(rel_path)  # Video URL'leri için kodlama yapıldı
            
            folder_name = rel_path.split('/')[0] if '/' in rel_path else "genel"

            # Excel'den gelen kazanım ve cevap bilgisi kontrolü
            q_str = str(q_num)
            excel_info = answer_keys.get(q_str, {})
            answer_val = excel_info.get("answer", "")
            kazanim_val = excel_info.get("kazanim", f"{folder_name.capitalize()} Soru {q_num} Video Çözümü")

            item = {
                "id": f"{publisher_prefix}_{global_id}",
                "lesson": folder_name.upper(),
                "questionNo": q_num,
                "answerKey": answer_val,  # Excel'den gelen cevap (Örn: "C")
                "videoFileName": file,
                "videoUrl": f"https://raw.githubusercontent.com/{github_username}/{repo_name}/main/{publisher_prefix}/{encoded_video_path}",
                "kazanimCode": f"{folder_name.upper()}-K{q_num}",
                "kazanimlar": [kazanim_val] if isinstance(kazanim_val, str) else kazanim_val
            }
            json_data.append(item)
            global_id += 1

# 3. ADIM: Ana Veriyi ve PDF Listesini Çıktı Olarak Kaydet
final_output = {
    "publisher": publisher_prefix,
    "pdfDocuments": pdf_files,
    "videos": json_data
}

output_file = f"{publisher_prefix}_full_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(final_output, f, ensure_ascii=False, indent=2)

print(f"\n[BAŞARILI] {len(json_data)} video ve {len(pdf_files)} PDF dosyası '{output_file}' dosyasına aktarıldı!\n")