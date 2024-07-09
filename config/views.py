from django.views.generic import ListView
from user.models import User 
class HomeView(ListView):
    model = User
    template_name = 'home.html'
    context_object_name = 'objects'