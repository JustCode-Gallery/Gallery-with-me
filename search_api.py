import os
import django
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import openai
from dotenv import load_dotenv
from asgiref.sync import sync_to_async
import logging

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from artwork.models import ArtWork, ArtTag, ArtWorkMaterial

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_data():
    # Django 데이터를 가져와 DataFrame 생성
    artworks = await sync_to_async(list)(ArtWork.objects.all().values('id', 'title', 'description', 'created_at'))
    tags = await sync_to_async(list)(ArtTag.objects.all().values('art_work_id', 'tag__name'))
    materials = await sync_to_async(list)(ArtWorkMaterial.objects.all().values('art_work_id', 'material__name'))

    # DataFrame 생성
    artworks_df = pd.DataFrame(artworks)
    tags_df = pd.DataFrame(tags).groupby('art_work_id')['tag__name'].apply(','.join).reset_index()
    materials_df = pd.DataFrame(materials).groupby('art_work_id')['material__name'].apply(','.join).reset_index()

    # artworks_df에 tags와 materials 병합
    artworks_df = artworks_df.merge(tags_df, left_on='id', right_on='art_work_id', how='left')
    artworks_df = artworks_df.merge(materials_df, left_on='id', right_on='art_work_id', how='left')

    # 빈 값 처리
    artworks_df['tag__name'] = artworks_df['tag__name'].fillna('')
    artworks_df['material__name'] = artworks_df['material__name'].fillna('')

    # 검색에 사용할 텍스트 필드 생성
    artworks_df['search_text'] = artworks_df.apply(
        lambda row: f"{row['title']} {row['description']} {row['tag__name']} {row['material__name']}",
        axis=1
    )

    # 로그로 search_text 필드 확인
    logger.info("Sample search_text: %s", artworks_df['search_text'].head())
    logger.info("Artworks DataFrame shape: %s", artworks_df.shape)

    return artworks_df

async def get_embeddings(texts):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return [embedding["embedding"] for embedding in response["data"]]

def cosine_similarity(a, b):
    return sum(x * y for x, y in zip(a, b)) / (sum(x**2 for x in a)**0.5 * sum(y**2 for y in b)**0.5)

@app.on_event("startup")
async def on_startup():
    global embeddings, artworks_df
    artworks_df = await get_data()
    embeddings = await get_embeddings(artworks_df['search_text'].tolist())

class SearchRequest(BaseModel):
    query: str

@app.post("/search/")
async def search_artworks(request: SearchRequest):
    try:
        query_embedding = (await get_embeddings([request.query]))[0]
        similarities = [(i, cosine_similarity(query_embedding, emb)) for i, emb in enumerate(embeddings)]
        similarities.sort(key=lambda x: x[1], reverse=True)

        # 유사도 기준 설정
        threshold = 0.78
        top_indices = [index for index, similarity in similarities if similarity >= threshold]
        
        results = artworks_df.iloc[top_indices] if top_indices else pd.DataFrame(columns=artworks_df.columns)

        # 검색 결과를 단순화된 형태로 변환
        simplified_results = results[['title']].to_dict(orient='records')

        # 로그로 각 작품의 유사도 값 확인
        for index, similarity in similarities:
            logger.info(f"Artwork ID: {artworks_df.iloc[index]['id']}, Title: {artworks_df.iloc[index]['title']}, Similarity: {similarity}")

        # 로그로 검색 결과 확인
        logger.info("Search results for query '%s': %s", request.query, simplified_results)

        return {"query": request.query, "results": simplified_results}
    except Exception as e:
        logger.error("Error during search: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
