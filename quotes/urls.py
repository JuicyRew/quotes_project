from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_quote, name='random_quote'),
    path('add', views.add_quote, name='add_quote'),
    path('quote/<int:pk>/', views.show_quote, name='show_quote'),
    path('<int:quote_id>/<str:action>/', views.vote, name='vote'),
    path('top/', views.top_quotes, name='top_quotes'),
    path('topics/', views.topics, name='topics')
]
