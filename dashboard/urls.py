from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns=[       
        path('', views.DashboardView.as_view(), name='home'),
        path('signup/', views.SignupPage.as_view(), name='signup'),
        path('accounts/login/', views.LoginPageView.as_view(), name='login'),
        path('logout/', views.LogoutView.as_view(), name='logout'),

        path('designations/', views.DesignationListView.as_view(), name='designations-list'),
        path('designations/create', views.DesignationCreateView.as_view(), name='designations-create'),
        path('designations/<int:pk>/update', views.DesignationUpdateView.as_view(), name='designations-update'),
        path('designations/<int:pk>/delete', views.DesignationDeleteView.as_view(), name='designations-delete'),
]