from django import template
from user.models import Seller
from artwork.models import ArtWork

register = template.Library()

@register.simple_tag
def verify_seller(user_id):
    return Seller.objects.filter(id=user_id).exists()

@register.simple_tag
def verify_owner(artwork_id, user_id):
    try:
        artwork = ArtWork.objects.get(id=artwork_id)
        return artwork.seller.id == user_id
    except ArtWork.DoesNotExist:
        return False