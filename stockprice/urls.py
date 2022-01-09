from django.urls import path
from . import views

urlpatterns = [
    path('stock_data/', views.get_stock_data, name='getstockdata'),
    path('predict/', views.get_predict_data, name='getpredictdata'),
]
