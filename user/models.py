from django.contrib.auth.models import AbstractUser
from django.db import models
# CNN모델 라이브러리
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from torch.nn.functional import softmax
import io

class User(AbstractUser):
    # 기본 사용자 모델에는 username, password, email, first_name, last_name 등 기본적인 필드들이 포함.
    # username은 식별자
    nickname = models.CharField(max_length=50)
    photo_url = models.ImageField()     # !이미지필드 경로추가
    phone_number = models.CharField(max_length=15)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    email = models.EmailField(unique=True)  # 이메일 중복 불가 설정
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # related_name 변경
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # related_name 변경
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )


class ShippingAddress(models.Model):
    recipient = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=15)
    destination = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=5)
    address = models.CharField(max_length=50)
    detail_address = models.CharField(max_length=50, null=True)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

class UserPreferArt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_work = models.ForeignKey('artwork.ArtWork', on_delete=models.CASCADE)

class University(models.Model):
    name = models.CharField(max_length=50)
    email_domain = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class University_Department(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.university.name}_{self.department.name}"

class Seller(User):
    bank = models.CharField(max_length=20)
    bank_user = models.CharField(max_length=20)
    account = models.CharField(max_length=20)  # 계좌번호는 문자열로 처리
    university_department = models.ForeignKey(University_Department, on_delete=models.SET_NULL, null=True)
    info = models.CharField(max_length=2000, null=True)

# CNN모델
class MultiOutputCNN(nn.Module):
    def __init__(self, num_artists, num_styles, num_genres, num_periods):
        super(MultiOutputCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(256 * 7 * 7, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout()
        )
        self.artist_classifier = nn.Linear(1024, num_artists)
        self.style_classifier = nn.Linear(1024, num_styles)
        self.genre_classifier = nn.Linear(1024, num_genres)
        self.period_classifier = nn.Linear(1024, num_periods)
    
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return (
            self.artist_classifier(x),
            self.style_classifier(x),
            self.genre_classifier(x),
            self.period_classifier(x)
        )


def load_model():
    num_artists = 2319
    num_styles = 137
    num_genres = 43
    num_periods = 6

    model = MultiOutputCNN(
        num_artists=num_artists,
        num_styles=num_styles,
        num_genres=num_genres,
        num_periods=num_periods
    )

    state_dict = torch.load('art_classifier/wikiart_multi_output_cnn.pth')  # CPU에서 로드

    # 예외적인 키를 처리
    unexpected_keys = ["classifier.3.weight", "classifier.3.bias"]
    for key in unexpected_keys:
        if key in state_dict:
            del state_dict[key]

    model.load_state_dict(state_dict, strict=False)
    model.eval()
    return model


def transform_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        image_tensor = transform(image)
        return image_tensor.unsqueeze(0)
    except Exception as e:
        raise ValueError(f"Image transformation error: {str(e)}")

def predict(image_tensor, model):
    model.eval()
    with torch.no_grad():
        outputs = model(image_tensor)
        artist_output, style_output, genre_output, period_output = outputs

        artist_probs = softmax(artist_output, dim=1)
        style_probs = softmax(style_output, dim=1)
        genre_probs = softmax(genre_output, dim=1)
        period_probs = softmax(period_output, dim=1)

        artist_prediction = torch.argmax(artist_probs, dim=1).item()
        style_prediction = torch.argmax(style_probs, dim=1).item()
        genre_prediction = torch.argmax(genre_probs, dim=1).item()
        period_prediction = torch.argmax(period_probs, dim=1).item()

    return {
        'artist': {
            'prediction': artist_prediction,
            'probability': artist_probs[0, artist_prediction].item()
        },
        'style': {
            'prediction': style_prediction,
            'probability': style_probs[0, style_prediction].item()
        },
        'genre': {
            'prediction': genre_prediction,
            'probability': genre_probs[0, genre_prediction].item()
        },
        'period': {
            'prediction': period_prediction,
            'probability': period_probs[0, period_prediction].item()
        }
    }
