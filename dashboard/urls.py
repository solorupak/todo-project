from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns=[       
        path('', views.DashboardView.as_view(), name='index'),
        
        # accounts
        path('accounts/signup/', views.SignupView.as_view(), name='signup'),
        path('accounts/login/', views.LoginPageView.as_view(), name='login'),
        path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
        path('accounts/change-password/', views.ChangePasswordView.as_view(), name='change-password'),

        path('designations/', views.DesignationListView.as_view(), name='designations-list'),
        path('designations/create', views.DesignationCreateView.as_view(), name='designations-create'),
        path('designations/<int:pk>/update', views.DesignationUpdateView.as_view(), name='designations-update'),
        path('designations/<int:pk>/delete', views.DesignationDeleteView.as_view(), name='designations-delete'),
]