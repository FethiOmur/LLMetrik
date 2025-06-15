#!/usr/bin/env python3

from ingestion.vector_store import VectorStore
from config.models import get_llm_model

def simple_cli():
    """Basit CLI arayüzü"""
    
    print('🚀 AMIF Grant Assistant - Basit CLI')
    print('=' * 60)
    print('AMIF hibe belgeleri hakkında sorularınızı sorun!')
    print('Çıkmak için "quit" yazın.')
    print('=' * 60)
    
    # Sistemleri başlat
    try:
        vector_store = VectorStore()
        llm = get_llm_model()
        
        count = vector_store.get_collection_count()
        print(f'✅ Sistem hazır! {count} belge yüklü.')
        print()
        
    except Exception as e:
        print(f'❌ Sistem başlatma hatası: {e}')
        return
    
    # Ana döngü
    while True:
        try:
            # Kullanıcı sorusu
            question = input('🤔 Sorunuz: ').strip()
            
            if question.lower() in ['quit', 'exit', 'çık', 'q']:
                print('👋 Görüşürüz!')
                break
            
            if not question:
                continue
            
            print('🔍 Aranıyor...')
            
            # Vector search
            results = vector_store.search(question, k=3)
            
            if not results:
                print('❌ İlgili bilgi bulunamadı.')
                continue
            
            print(f'📊 {len(results)} sonuç bulundu')
            
            # LLM ile cevap oluştur
            context = "\n\n".join(results[:2])  # İlk 2 sonucu kullan
            
            prompt = f"""Sen AMIF (Asylum, Migration and Integration Fund) hibe programı konusunda uzman bir asistansın. 
Aşağıdaki bağlam bilgilerini kullanarak kullanıcının sorusunu Türkçe olarak yanıtla.

Bağlam:
{context}

Soru: {question}

Lütfen net, anlaşılır ve faydalı bir yanıt ver. Eğer bağlamda yeterli bilgi yoksa, bunu belirt."""
            
            print('🤖 Yanıt hazırlanıyor...')
            
            try:
                response = llm.invoke(prompt)
                print('\n💡 Yanıt:')
                print('-' * 40)
                print(response.content)
                print('-' * 40)
                print()
                
            except Exception as e:
                print(f'❌ LLM hatası: {e}')
                print('📄 Ham sonuçlar:')
                for i, result in enumerate(results[:2], 1):
                    print(f'{i}. {result[:300]}...')
                print()
                
        except KeyboardInterrupt:
            print('\n👋 Görüşürüz!')
            break
        except Exception as e:
            print(f'❌ Hata: {e}')
            continue

if __name__ == "__main__":
    simple_cli() 