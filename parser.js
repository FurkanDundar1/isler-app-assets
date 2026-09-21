const fs = require('fs');
const path = require('path');

// Bu script bulunduğu klasördeki videoları tarar
const targetFolder = path.join(__dirname, 'Acil Yayınları Örnek', 'acil-tyt-ayt-2025 video çözümler');

if (!fs.existsSync(targetFolder)) {
  console.log('Klasör bulunamadı, lütfen klasör adını kontrol et!');
  process.exit();
}

const files = fs.readdirSync(targetFolder);
const videoData = [];

files.forEach((file) => {
  if (file.endsWith('.mp4')) {
    videoData.push({
      fileName: file,
      publisher: 'Acil Yayınları',
      // Video linki ileride buraya gelecek:
      videoUrl: '' 
    });
  }
});

fs.writeFileSync('acil_videolar.json', JSON.stringify(videoData, null, 2));
console.log('İşlem tamam! acil_videolar.json dosyası oluşturuldu.');