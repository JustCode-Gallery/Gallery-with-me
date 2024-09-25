from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import torch
from torchvision import transforms
from PIL import Image
import io
import json
from typing import Dict
  
import os
import django

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from user.models import MultiOutputCNN

try:
    with open('art_classifier/mapping_info.json', 'r') as f:
        mapping_info = json.load(f)
except FileNotFoundError:
    raise Exception("Mapping info file not found. Please ensure 'art_classifier/mapping_info.json' exists.")


# 매핑 로드
idx_to_artist = mapping_info["idx_to_artist"]
idx_to_style = mapping_info["idx_to_style"]
idx_to_genre = mapping_info["idx_to_genre"]
idx_to_period = mapping_info["idx_to_period"]

# 학습 시 사용한 클래스 수를 그대로 가져와서 사용
# 실제 학습된 데이터셋의 클래스 수로 변경
num_artists = len(idx_to_artist)  # 실제 artist 클래스 수
num_styles = len(idx_to_style)    # 실제 style 클래스 수
num_genres = len(idx_to_genre)    # 실제 genre 클래스 수
num_periods = len(idx_to_period)  # 실제 period 클래스 수

# 모델 초기화 (가중치만 로드)
model = MultiOutputCNN(num_artists, num_styles, num_genres, num_periods)
model.load_state_dict(torch.load('art_classifier/wikiart_multi_output_cnn.pth', map_location=torch.device('cpu')))
model.eval()

app = FastAPI()

class Prediction(BaseModel):
    artist: Dict[str, float]
    style: Dict[str, float]
    genre: Dict[str, float]
    period: Dict[str, float]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.post("/predict/", response_model=Prediction)
async def predict(file: UploadFile = File(...)):
    try:
        # 업로드된 이미지 읽기 및 변환
        image = Image.open(io.BytesIO(await file.read())).convert('RGB')
        image = transform(image).unsqueeze(0)

        # 모델 추론
        with torch.no_grad():
            artist_output, style_output, genre_output, period_output = model(image)

        # softmax 함수로 확률 계산
        artist_probs = torch.softmax(artist_output, dim=1).squeeze()
        style_probs = torch.softmax(style_output, dim=1).squeeze()
        genre_probs = torch.softmax(genre_output, dim=1).squeeze()
        period_probs = torch.softmax(period_output, dim=1).squeeze()

        # 예측된 클래스 인덱스와 확률 가져오기
        artist_pred = artist_probs.argmax().item()
        style_pred = style_probs.argmax().item()
        genre_pred = genre_probs.argmax().item()
        period_pred = period_probs.argmax().item()

         # 실제 레이블 이름으로 변환
        artist_name = idx_to_artist[str(artist_pred)]
        style_name = idx_to_style[str(style_pred)]
        genre_name = idx_to_genre[str(genre_pred)]
        period_name = idx_to_period[str(period_pred)]


        # 예측 결과 반환 (인덱스 및 확률 포함)
        return Prediction(
            artist={artist_name: artist_probs[artist_pred].item()},
            style={style_name: style_probs[style_pred].item()},
            genre={genre_name: genre_probs[genre_pred].item()},
            period={period_name: period_probs[period_pred].item()},
        )
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8900)
