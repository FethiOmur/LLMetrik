# 🚀 AMIF Grant Assistant - LangGraph Multi-Agent Chatbot

Bu proje, AMIF (Asylum, Migration and Integration Fund) hibe belgeleri için geliştirilmiş akıllı bir soru-cevap sistemidir. LangGraph tabanlı multi-agent mimarisi kullanarak PDF belgeleri analiz eder ve kullanıcı sorularına kaynak belirtme ile yanıt verir.

## ✨ Özellikler

- **PDF İngestion**: 49 AMIF belgesi (5,037 sayfa, 13M+ karakter) işlendi
- **Multi-Agent Mimarisi**: LangGraph ile orchestrated ajanlar
- **Gelişmiş Vektör Arama**: ChromaDB ile semantik arama
- **Kaynak Belirtme**: Her yanıt için PDF dosya adı ve sayfa numarası
- **Çok Dil Desteği**: Türkçe/İngilizce otomatik dil algılama
- **Çoklu Arayüz**: CLI, Advanced CLI, Streamlit web arayüzü

## 🔧 Teknik Stack

- **LangGraph**: Agent orchestration
- **OpenAI GPT-4**: Response generation
- **text-embedding-3-small**: Vector embeddings
- **ChromaDB**: Vector database
- **Streamlit**: Web interface
- **PyMuPDF**: PDF processing

## 📊 Performans

- 17,293 text chunk işlendi
- ~2-3 saniye yanıt süresi
- Sorgu başına 8 kaynak ile sayfa belirtme
- Otomatik dil algılama ve yanıt eşleştirme

## 🚀 Kurulum

### 1. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 2. OpenAI API Key
`config/models.py` dosyasında API key'inizi ayarlayın:
```python
OPENAI_API_KEY = "your-api-key-here"
```

### 3. PDF Belgelerini Yükle
PDF dosyalarınızı `data/raw/` klasörüne koyun.

### 4. Vektör Veritabanını Oluştur
```bash
python3 -c "
from ingestion.vector_store import VectorStore
from ingestion.pdf_loader import PDFLoader
from ingestion.text_processor import TextProcessor

vs = VectorStore()
loader = PDFLoader()
processor = TextProcessor()

docs = loader.load_all_pdfs('data/raw')
processed = processor.process_documents(docs)
vs.add_documents(processed)
"
```

## 💻 Kullanım

### Başlatma Menüsü
```bash
python3 start.py
```

### Direkt Arayüzler

#### 1. Advanced CLI
```bash
python3 advanced_cli.py
```

#### 2. Streamlit Web App
```bash
streamlit run streamlit_app.py
```

#### 3. Simple CLI
```bash
python3 simple_cli.py
```

## 📁 Proje Yapısı

```
GrantSpider/
├── agents/          # LangGraph ajanları
├── chains/          # LangChain zincir mantığı
├── config/          # Model ve ayar konfigürasyonları
├── data/            # PDF dosyaları ve vektör DB
├── graph/           # LangGraph graf tanımları
├── ingestion/       # PDF yükleme ve vektör işleme
├── interfaces/      # Kullanıcı arayüzleri
├── memory/          # Konuşma hafızası
└── utils/           # Yardımcı fonksiyonlar
```

## 📋 Workspace Kuralları

Proje modüler yapıyı korumak için şu kurallara uyar:

1. **PDF işleme** → yalnızca `ingestion/` klasöründe
2. **Agent mantığı** → yalnızca `agents/` klasöründe  
3. **Graf tanımları** → yalnızca `graph/` klasöründe
4. **Kullanıcı arayüzü** → yalnızca `interfaces/` klasöründe

## 🔍 Örnek Kullanım

```
🤔 Sorunuz: What are the personnel cost calculation requirements?

💡 YANIT:
Personnel costs are calculated using a daily rate formula:
Daily rate = annual personnel costs / 215

📚 KAYNAKLAR:
[1] AMIF-2025-TF2-AG-INTE-01-WOMEN_separator_aga_en.pdf (Sayfa: 54)
[2] AMIF-2025-TF2-AG-INTE-02-HEALTH_separator_aga_en.pdf (Sayfa: 54)
```

## 📈 Gelişmiş Özellikler

- **Kaynak Doğrulama**: Her yanıt gerçek PDF sayfa referansları ile
- **Dil Adaptasyonu**: Soru dilinde otomatik yanıt
- **Metadata Zenginleştirme**: Dosya boyutu, sayfa sayısı, chunk bilgileri
- **Performans Optimizasyonu**: Paralel işleme ve cache mekanizması

## 📝 Lisans

MIT License

## 👥 Katkıda Bulun

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

**Not**: Bu sistem EU grant belgelerinin karmaşık yapısını analiz etmek için optimize edilmiştir. Farklı belge türleri için ingestion pipeline'ı ayarlanabilir. 