from django import template

register = template.Library()

@register.filter
def format_currency(value):
    try:
        value = int(value)  # 소수점 이하를 제거하여 정수로 변환
        return "{:,}원".format(value)  # 쉼표를 추가하여 포맷
    except (ValueError, TypeError):
        return value