from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView, InvestmentCreateView, MyInvestmentsView

urlpatterns = [
    path('', ProjectListCreateView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('invest/', InvestmentCreateView.as_view(), name='invest'),
    path('my-investments/', MyInvestmentsView.as_view(), name='my-investments'),
]
