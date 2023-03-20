from django.urls import path
from .views import (
    sale_list,
    new_sale,
    sale_detail,
    sale_update,
    restaurant_sale_report
)

urlpatterns = [
    path('', sale_list, name='sale_list'),
    path('new/', new_sale, name='new_sale'),
    path('<int:pk>/', sale_detail, name='sale_detail'),
    path('<int:pk>/edit/', sale_update, name='sale_update'),
    path('restaurant_sale_report', restaurant_sale_report, name='restaurant_sale_report'),
]
