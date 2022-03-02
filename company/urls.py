from django.urls import path

from company.views import CompanyAPIView, CompanyDetailAPIView, StarCompanyInternView

# , StarCompanyAPIView

# Company views
urlpatterns = [
    path('', CompanyAPIView.as_view(), name='company'),
    # path('<int:pk>/', company_update, name='company_detail'),
    path('<int:pk>/', CompanyDetailAPIView.as_view(), name='company_detail'),
    path('star/', StarCompanyInternView.as_view(), name='company_star'),
    # TODO path active PUT/GET
]