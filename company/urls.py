from django.urls import path

from company.views import CompanyAPIView, CompanyActiveEmployeesAPIView, CompanyActiveInternView, CompanyDetailAPIView, CompanyMetricsView, CompanyStarInternView, CustomQueryAPIView

"""
Routes related to
    path('company/', include('company.urls'))
From clorusapi.urls.py
"""

# Company views
urlpatterns = [
    path('', CompanyAPIView.as_view(), name='company'),
    # path('<int:pk>/', company_update, name='company_detail'),
    path('<int:pk>/', CompanyDetailAPIView.as_view(), name='company_detail'),
    path('active/', CompanyActiveInternView.as_view(), name='company_active'),
    path('active/employees/', CompanyActiveEmployeesAPIView.as_view(), name='company_active_employees'),
    path('metrics/', CompanyMetricsView.as_view(), name='company_metrics'),
    path('star/', CompanyStarInternView.as_view(), name='company_star'),
    path('queries/', CustomQueryAPIView.as_view(), name='company_queries'),
    # TODO path active PUT/GET
]