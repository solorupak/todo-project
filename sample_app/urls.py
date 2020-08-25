from django.urls import path
from .views import *

app_name = 'sample_app'

urlpatterns=[       
        path('', DashboardView.as_view(), name='home'),
        path('signup/', SignupPage.as_view(), name='signup'),
        path('accounts/login/', LoginPage.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),

        path('designation/list/',DesignationList.as_view(), name='designation-list'),
        path('designation/create/',DesignationCreate.as_view(), name='designation-create'),
        path('designation/<int:pk>/update/',DesignationUpdate.as_view(), name='designation-update'),
        path('designation/<int:pk>/delete/',DesignationDelete.as_view(), name='designation-delete'),
]