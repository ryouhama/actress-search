from django.urls import path
from . import views
from webapp.views import TopView


urlpatterns = [
    path(r'top/', TopView.as_view(template_name='top.html'), name='top'),
    path(r'search/', views.search_action_and_send_list, name='search'),
]