import { NextResponse } from 'next/server';
import { NewsService } from '@/lib/services';

// GET /api/news
export async function GET(request: Request) {
  try {
    // URL parametrelerini al
    const { searchParams } = new URL(request.url);
    const slug = searchParams.get('slug');
    const tag = searchParams.get('tag');
    const limit = searchParams.get('limit');
    
    // Slug ile arama yapılıyorsa tek bir haberi getir
    if (slug) {
      const news = await NewsService.getNewsBySlug(slug);
      if (!news) {
        return NextResponse.json(
          { error: 'News not found' },
          { status: 404 }
        );
      }
      return NextResponse.json(news);
    }
    
    // Etiket ile arama yapılıyorsa haberleri etiket ile getir
    if (tag) {
      const news = await NewsService.getNewsByTag(tag);
      return NextResponse.json(news);
    }
    
    // Limit belirtilmişse son n haberi getir
    if (limit) {
      const limitNum = parseInt(limit, 10);
      const news = await NewsService.getLatestNews(limitNum);
      return NextResponse.json(news);
    }
    
    // Parametre yoksa tüm haberleri getir
    const allNews = await NewsService.getAllNews();
    return NextResponse.json(allNews);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// POST /api/news - Yeni haber oluştur
export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // Gerekli alanları kontrol et
    if (!body.title || !body.description || !body.summary || !body.image) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }
    
    // Yeni haber oluştur
    const newNews = await NewsService.createNews(body);
    
    if (!newNews) {
      return NextResponse.json(
        { error: 'Failed to create news' },
        { status: 500 }
      );
    }
    
    return NextResponse.json(newNews, { status: 201 });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 