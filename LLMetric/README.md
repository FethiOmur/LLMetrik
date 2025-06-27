# LLMetric

LLMetric, farklı Büyük Dil Modellerini (LLM) karşılaştırma ve bilgi sunma amacıyla geliştirilmiş bir web uygulamasıdır.

## 🚀 Özellikler

- LLM modelleri karşılaştırma
- LLM dünyasından en son haberler
- Model arama ve filtreleme
- Ayrıntılı haber sayfaları

## 🛠️ Teknoloji Yığını

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **UI Bileşenleri**: Shadcn/UI
- **Veritabanı**: Supabase (ileride uygulanacak)
- **Deploymen**t: Vercel

## 📂 Proje Yapısı

```
LLMetric/
├── app/                 # Next.js 13 App Router
│   ├── api/             # API rotaları
│   ├── components/      # Sayfa komponenleri
│   ├── data/            # Statik veriler
│   ├── news/            # Haber sayfaları
│   └── page.tsx         # Ana sayfa
├── components/          # Yeniden kullanılabilir UI bileşenleri
│   └── ui/              # Temel UI bileşenleri (shadcn)
├── lib/                 # Yardımcı fonksiyonlar ve servisler
│   ├── services/        # Servis katmanı
│   ├── supabase/        # Supabase entegrasyonu (ileride)
│   └── utils.ts         # Yardımcı fonksiyonlar
├── public/              # Statik dosyalar
└── styles/              # Global stiller
```

## 🏛️ Mimari Yapı

Bu proje, Next.js 13 App Router kullanılarak geliştirilmiştir ve modern web geliştirme prensiplerine uygun olarak tasarlanmıştır.

### Veri Akışı

1. **Statik Veriler**: Geliştirme aşamasında veriler `/app/data` içindeki TS dosyalarından gelir
2. **Servis Katmanı**: `/lib/services` içindeki servis sınıfları verilere erişim sağlar
3. **API Rotaları**: `/app/api` altındaki route.ts dosyaları servisleri kullanarak veri sunar
4. **Bileşenler**: Veriler servisleri kullanarak render edilir

### Supabase Entegrasyonu (İleride)

Proje, gelecekte statik verilerden Supabase veritabanına geçiş yapacak şekilde tasarlanmıştır:

1. Tüm veri erişimi servis katmanı üzerinden yapılır
2. Servis fonksiyonları, Supabase'e geçiş için hazır yorumlanmış kod içerir
3. Veri şemaları `/lib/supabase/config.ts` içinde tanımlanmıştır

## 🚀 Başlangıç

### Gereksinimler

- Node.js 18+
- pnpm (önerilen) veya npm

### Kurulum

```bash
# Depoyu klonla
git clone https://github.com/yourusername/llmetric.git
cd llmetric

# Bağımlılıkları yükle
pnpm install

# Geliştirme sunucusunu başlat
pnpm dev
```

### Ortam Değişkenleri

İleride Supabase entegrasyonu için aşağıdaki ortam değişkenlerini `.env.local` dosyasına ekleyin:

```
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...
```

## 🧩 Katkıda Bulunma

1. Repoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'e push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun 