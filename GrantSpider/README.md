# 🚀 AMIF Grant Assistant

AMIF (Asylum, Migration and Integration Fund) hibe belgeleri için akıllı soru-cevap sistemi. LangGraph tabanlı multi-agent chatbot ile PDF belgelerinden semantik arama ve kaynak atıfları.

## ✨ Özellikler

- 📄 **PDF Belge İşleme**: 49 AMIF hibe belgesi yüklü (7,400+ metin parçası)
- 🔍 **Semantik Arama**: OpenAI embeddings ile gelişmiş arama
- 🤖 **AI Asistan**: GPT-4 ile akıllı yanıtlar
- 📚 **Kaynak Atıfları**: Her yanıt için PDF kaynağı ve sayfa numarası
- 🎨 **Çoklu Arayüz**: CLI ve Streamlit web arayüzü
- 🌐 **Çok Dilli**: Türkçe ve İngilizce destek

## 🏗️ Sistem Mimarisi

```
GrantSpider/
├── config/          # API anahtarları ve model konfigürasyonları
├── ingestion/       # PDF yükleme, metin işleme, vektör veritabanı
├── agents/          # LangGraph ajanları (retriever, qa_agent, supervisor)
├── memory/          # Konuşma hafızası yönetimi
├── chains/          # LangChain zincirleri
├── graph/           # Multi-agent graph tanımları
├── interfaces/      # Kullanıcı arayüzleri
├── utils/           # Yardımcı fonksiyonlar
└── data/            # PDF dosyaları ve vektör veritabanı
```

## 🚀 Kurulum

### 1. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 2. Environment Variables Oluştur
Proje kök dizininde `.env` dosyası oluşturun:

```bash
# .env dosyası
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_DB_PATH=data/db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
DEBUG=False
```

**⚠️ Önemli**: `.env` dosyası git'e commit edilmez, bu güvenlik içindir.

### 3. PDF Belgelerini Yükle
PDF dosyalarınızı `data/raw/` klasörüne koyun ve sistemi çalıştırın.

## 💻 Kullanım

### CLI Arayüzü (Gelişmiş)
```bash
python3 advanced_cli.py
```

**Özellikler:**
- 🎨 Renkli terminal arayüzü
- 📚 Kaynak bilgileri gösterimi
- ⏰ Zaman damgaları
- 💡 Yardım menüsü
- 🧹 Ekran temizleme

### Streamlit Web Arayüzü
```bash
streamlit run streamlit_app.py
```

**Özellikler:**
- 🌐 Modern web arayüzü
- 📊 Sistem durumu gösterimi
- 💡 Örnek sorular
- 📚 Detaylı kaynak bilgileri
- 🔍 Ham arama sonuçları

### Basit CLI
```bash
python3 simple_cli.py
```

## 📋 Örnek Sorular

- "AMIF hibe başvurusu nasıl yapılır?"
- "What are the eligibility criteria for AMIF grants?"
- "Proje bütçesi nasıl hazırlanmalı?"
- "Subcontracting rules nelerdir?"
- "Application deadline ne zaman?"
- "Hangi ülkeler başvurabilir?"

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler
- **LangChain**: Belge işleme ve AI zinciri
- **LangGraph**: Multi-agent workflow
- **OpenAI GPT-4**: Dil modeli
- **OpenAI Embeddings**: Metin vektörleştirme
- **ChromaDB**: Vektör veritabanı
- **PyMuPDF**: PDF işleme
- **Streamlit**: Web arayüzü

### Veri İşleme Pipeline
1. **PDF Yükleme**: PyMuPDF ile PDF'leri metin olarak çıkarma
2. **Metin Bölme**: RecursiveCharacterTextSplitter ile chunking
3. **Vektörleştirme**: OpenAI embeddings ile vektör oluşturma
4. **Depolama**: ChromaDB'de kalıcı saklama
5. **Arama**: Semantik benzerlik araması
6. **Yanıt**: GPT-4 ile bağlamsal yanıt oluşturma

### Performans
- 📊 **7,413 belge** vektör veritabanında
- ⚡ **~2-3 saniye** yanıt süresi
- 🎯 **Yüksek doğruluk** kaynak atıfları ile
- 💾 **Düşük bellek** kullanımı

## 📚 Kaynak Atıfları

Sistem her yanıt için şu bilgileri sağlar:
- 📄 **PDF Dosya Adı**: Hangi belgeden geldiği
- 📍 **Sayfa Numarası**: Bilginin bulunduğu sayfa
- 🔍 **İlgililik Skoru**: Semantic search sonucu

## 🛠️ Geliştirme

### Test Etme
```bash
# Sistem testi
python3 test_full_system.py

# Vector store testi
python3 test_vector_store.py
```

### Yeni PDF Ekleme
1. PDF'leri `data/raw/` klasörüne koyun
2. `load_pdfs_to_vector_store.py` scriptini çalıştırın

## 📈 Gelecek Özellikler

- 🔄 **Multi-Agent Workflow**: LangGraph ile gelişmiş ajan sistemi
- 💾 **Konuşma Hafızası**: Önceki sorular için bağlam
- 🌍 **Çok Dilli Destek**: Daha fazla dil desteği
- 📊 **Analytics Dashboard**: Kullanım istatistikleri
- 🔐 **Kullanıcı Yönetimi**: Kimlik doğrulama sistemi

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🙏 Teşekkürler

- OpenAI GPT-4 ve Embeddings API
- LangChain ve LangGraph ekibi
- ChromaDB geliştiricileri
- Streamlit topluluğu

---

**🚀 AMIF Grant Assistant** - Powered by AI, Built with ❤️ 