from django import template
from user.models import Seller

register = template.Library()

@register.simple_tag
def verify_seller(user_id):
    return Seller.objects.filter(id=user_id).exists()
