from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import RegisterView, LoginView, ProfileView
from projects.views import (
    ProjectListCreateView, ProjectDetailView, InvestmentCreateView,
    MyInvestmentsView, AcceptInvestmentView, RejectInvestmentView, ProjectInvestmentsView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    
    # Projets
    path('api/projects/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('api/projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('api/projects/<int:pk>/investments/', ProjectInvestmentsView.as_view(), name='project_investments'),
    
    # Investissements
    path('api/investments/create/', InvestmentCreateView.as_view(), name='investment_create'),
    path('api/investments/my/', MyInvestmentsView.as_view(), name='my_investments'),
    path('api/investments/<int:pk>/accept/', AcceptInvestmentView.as_view(), name='accept_investment'),
    path('api/investments/<int:pk>/reject/', RejectInvestmentView.as_view(), name='reject_investment'),
]
