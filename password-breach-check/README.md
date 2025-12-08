# Password Breach Check – K-Anonimlik Tabanlı Parola İhlal Kontrolü  
**Siber Güvenlik Dönem Sonu Projesi • Python – HaveIBeenPwned API**

Bu proje, kullanıcı parolalarının *haveibeenpwned (HIBP) Pwned Passwords* veritabanına **K-anonimlik prensibi** ile gönderilmeden, gizlilik korunarak ihlal edilip edilmediğini kontrol eden bir sistem sunar.  

Proje üç ana bileşenden oluşur:

- **Komut satırı arayüzü (CLI)**
- **Modern grafik arayüz (GUI – CustomTkinter)**
- **Modüler Python mimarisi + birim testleri**

---

## Özellikler

### **K-Anonim Parola Kontrolü**
- Parolanın SHA-1 hash'i çıkarılır  
- İlk 5 karakter (“prefix”) HIBP API'ye gönderilir  
- API’den dönen suffix listesinde tam eşleşme aranır  
- Parola **asla ağ üzerinden gönderilmez**

### **Gizlilik ve Güvenlik**
- Parola veya hash değerleri loglanmaz  
- Hatalar güvenli şekilde yönetilir  
- API rate limit hataları ele alınır  

### **GUI (CustomTkinter)**
- Modern kart tasarımı  
- Tema seçici (Light / Dark / System)  
- Parola göster/gizle  
- Parola güç göstergesi (progress bar)  
- Sonuçların panel içinde gösterimi  

### **Testler**
- SHA-1 hash testi  
- Prefix–suffix bölme  
- HIBP API mock testleri  
- Parola pwned/not-pwned senaryoları  
- Parola güç analiz testleri  

---

## Proje Yapısı

```text
password-breach-check/
├─ src/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ hibp_client.py      # HIBP K-anon API istemcisi
│  ├─ checker.py          # SHA-1, pwned check, strength analyzer
│  └─ gui_app.py          # Modern GUI arayüzü
│  └─ main.py             # CLI arayüzü
│
├─ tests/
│  ├─ conftest.py
│  ├─ test_hashing.py
│  ├─ test_checker.py
│  ├─ test_hibpclient.py
│  ├─ test_strength.py
│  └─ test_utils.py
│  └─ test_parse.py
│
├─ requirements.txt
├─ README.md
├─ LICENSE
└─ .gitignore
```
---

## Kurulum

### **1) Sanal Ortam (Önerilir)**

```bash
python -m venv venv
.\venv\Scripts\activate     # Windows
```

### **2) Bağımlılıkların yüklenmesi**

```bash
pip install -r requirements.txt
```

### **3) Testlerin çalıştırılması**

```bash
pytest
```
---

## Kullanım

### **CLI (Terminal Arayüzü)**

```bash
python -m src.main
```

### **JSON çıktı almak için:**

```bash
python -m src.main --json
```

## GUI (Grafik Arayüz)

GUI’yi başlatmak için:
```bash
python -m src.gui_app
```
---

### **Arayüz özellikleri:**

- Parola girişi
- Parola göster/gizle
- Light/Dark tema
- Parola güç analizi
- HIBP K-anon kontrol sonucu

---

## Parola Güç Analizi

Kod, girilen parola üzerinde aşağıdaki kriterlere göre değerlendirme yapar:

- Uzunluk
- Küçük harf – büyük harf
- Rakam
- Özel karakter
- 0–4 arası skor
- “çok zayıf / zayıf / orta / güçlü / çok güçlü” etiketi
- GUI arayüzünde progress bar ile görselleştirilir.

---

## K-Anonimlik Nasıl Çalışır?

1. Parola SHA-1 ile hashlenir
2. Hash'in ilk 5 karakteri (prefix) API’ye gönderilir
3. API, o prefix ile başlayan tüm suffix’leri döner
4. Gerçek hash suffix'i ile tam eşleşme aranır
5. Parolayı kendisi asla gönderilmediği için gizlilik korunur

Bu model HIBP tarafından kullanılan ve sektör standardı kabul edilen bir gizlilik yöntemidir.

---

## Güvenlik Notları

- Hassas bilgiler loglanmaz
- API isteği sırasında TLS zorunludur
- “Add-Padding” header’ı ile istenirse daha güçlü gizlilik sağlanabilir
- GUI ve CLI üzerinde parola görüntüleme/gizleme desteği bulunur

---

## Lisans

Proje MIT lisansı ile paylaşılmıştır.

---

## Geliştiren

211805066 Birgül Yüksel -  Adü Siber Güvenlik Dersi Öğrencisi

---