from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
# Create your views here.

# @login_required
# def cart(request):
#     if request.method == 'POST':
#         selected_items = request.POST.getlist('selected_items')
#         if not selected_items:
#             return render(request, 'order/cart.html', {'error': 'No items selected', 'cart_items': Cart.objects.filter(user=request.user)})

#         # Process the selected items for checkout
#         # This is where you would handle the payment process, create an order, etc.
#         # For now, we'll just redirect to a success page

#         # Example: Create an order and redirect to a success page
#         # order = Order.objects.create(user=request.user, ...)
#         # for item_id in selected_items:
#         #     cart_item = Cart.objects.get(id=item_id)
#         #     OrderItem.objects.create(order=order, art_work=cart_item.art_work, quantity=cart_item.quantity, ...)
#         # cart_item.delete()

#         return redirect('order:checkout_success')
