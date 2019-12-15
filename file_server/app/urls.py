from django.urls import path, register_converter
from app.views import file_list, file_content
from app.converter import DateConverter


register_converter(DateConverter, 'date')

urlpatterns = [
    path('', file_list, name='file_list'),
    path('<date:date>/', file_list, name='file_list'),
    path('<name>/', file_content, name='file_content'),
]
