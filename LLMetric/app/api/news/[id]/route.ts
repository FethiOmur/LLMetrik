import { NextResponse } from 'next/server';
import { NewsService } from '@/lib/services';

// Belirli bir ID'ye sahip haberi getirme, düzenleme ve silme

interface RouteParams {
  params: Promise<{
    id: string;
  }>;
}

// GET /api/news/:id
export async function GET(request: Request, { params }: RouteParams) {
  try {
    const resolvedParams = await params;
    const { id } = resolvedParams;
    
    // Şu anda slug ile çalışıyoruz, gelecekte ID ile çalışacağız
    const news = await NewsService.getNewsBySlug(id);
    
    if (!news) {
      return NextResponse.json(
        { error: 'News not found' },
        { status: 404 }
      );
    }
    
    return NextResponse.json(news);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// PUT /api/news/:id - Haberi güncelle
export async function PUT(request: Request, { params }: RouteParams) {
  try {
    const resolvedParams = await params;
    const { id } = resolvedParams;
    const body = await request.json();
    
    // Gerekli alanları kontrol et
    if (Object.keys(body).length === 0) {
      return NextResponse.json(
        { error: 'No fields to update' },
        { status: 400 }
      );
    }
    
    // Haberi güncelle
    const updatedNews = await NewsService.updateNews(id, body);
    
    if (!updatedNews) {
      return NextResponse.json(
        { error: 'Failed to update news or news not found' },
        { status: 404 }
      );
    }
    
    return NextResponse.json(updatedNews);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// DELETE /api/news/:id - Haberi sil
export async function DELETE(_request: Request, { params }: RouteParams) {
  try {
    const resolvedParams = await params;
    const { id } = resolvedParams;
    
    // Haberi sil
    const success = await NewsService.deleteNews(id);
    
    if (!success) {
      return NextResponse.json(
        { error: 'Failed to delete news or news not found' },
        { status: 404 }
      );
    }
    
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 