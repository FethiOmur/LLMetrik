import { NextResponse } from 'next/server';
import { ModelsService, NewsService } from '@/lib/services';

// GET /api/models/related - Bir haber ile ilgili modelleri getir
export async function GET(request: Request) {
  try {
    // URL parametrelerini al
    const { searchParams } = new URL(request.url);
    const newsSlug = searchParams.get('news');
    const limit = searchParams.get('limit') || '3';
    
    if (!newsSlug) {
      return NextResponse.json(
        { error: 'News slug is required' },
        { status: 400 }
      );
    }
    
    // Haberi getir
    const news = await NewsService.getNewsBySlug(newsSlug);
    
    if (!news) {
      return NextResponse.json(
        { error: 'News not found' },
        { status: 404 }
      );
    }
    
    // İlgili modelleri getir
    const limitNum = parseInt(limit, 10);
    const relatedModels = await ModelsService.getRelatedModels(news, limitNum);
    
    return NextResponse.json(relatedModels);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 