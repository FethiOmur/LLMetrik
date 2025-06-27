import { NextResponse } from 'next/server';
import { ModelsService } from '@/lib/services';

// GET /api/models
export async function GET(request: Request) {
  try {
    // URL parametrelerini al
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');
    const keyword = searchParams.get('keyword');
    const limit = searchParams.get('limit');
    
    // ID ile arama yapılıyorsa tek bir modeli getir
    if (id) {
      const model = await ModelsService.getModelById(id);
      if (!model) {
        return NextResponse.json(
          { error: 'Model not found' },
          { status: 404 }
        );
      }
      return NextResponse.json(model);
    }
    
    // Anahtar kelime ile arama yapılıyorsa modelleri getir
    if (keyword) {
      const models = await ModelsService.getModelsByKeyword(keyword);
      return NextResponse.json(models);
    }
    
    // Limit belirtilmişse popüler modelleri getir
    if (limit) {
      const limitNum = parseInt(limit, 10);
      const models = await ModelsService.getPopularModels(limitNum);
      return NextResponse.json(models);
    }
    
    // Parametre yoksa tüm modelleri getir
    const allModels = await ModelsService.getAllModels();
    return NextResponse.json(allModels);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 