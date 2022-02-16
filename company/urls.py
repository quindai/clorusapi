from django.urls import path

from company.views import CompanyAPIView, CompanyDetailAPIView

# Company views
urlpatterns = [
    path('', CompanyAPIView.as_view(), name='company'),
    path('<int:pk>/', CompanyDetailAPIView.as_view(), name='company_detail'),
    
]