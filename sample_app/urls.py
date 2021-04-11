from django.urls import path
from .views import *

app_name = 'sample_app'

urlpatterns=[       
        path('', DashboardView.as_view(), name='home'),
        path('signup/', SignupPage.as_view(), name='signup'),
        path('accounts/login/', LoginPageView.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),

        path('designation/',DesignationListView.as_view(), name='designation-list'),
        path('designation/create/',DesignationCreateView.as_view(), name='designation-create'),
        path('designation/<int:pk>/update/',DesignationUpdateView.as_view(), name='designation-update'),
        path('designation/<int:pk>/delete/',DesignationDeleteView.as_view(), name='designation-delete'),
]