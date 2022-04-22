from django.urls import path

from company.views import CompanyAPIView, CompanyActiveInternView, CompanyDetailAPIView, CompanyMetricsView, CompanyStarInternView

# , StarCompanyAPIView

# Company views
urlpatterns = [
    path('', CompanyAPIView.as_view(), name='company'),
    # path('<int:pk>/', company_update, name='company_detail'),
    path('<int:pk>/', CompanyDetailAPIView.as_view(), name='company_detail'),
    path('active/', CompanyActiveInternView.as_view(), name='company_active'),
    path('metrics/', CompanyMetricsView.as_view(), name='company_metrics'),
    path('star/', CompanyStarInternView.as_view(), name='company_star'),
    # TODO path active PUT/GET
]