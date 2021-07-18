from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),

    # git-pull
    path('git-pull', views.GitPullView.as_view(), name='git-pull'),

    # audit-trail
    path('audits', views.AuditTrailListView.as_view(), name='audittrail-list'),

    # accounts
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/login/', views.LoginPageView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/change-password/',
         views.ChangePasswordView.as_view(), name='change-password'),

    # designation crud
    path('designations/', views.DesignationListView.as_view(),
         name='designations-list'),
    path('designations/create', views.DesignationCreateView.as_view(),
         name='designations-create'),
    path('designations/<int:pk>/update',
         views.DesignationUpdateView.as_view(), name='designations-update'),
    path('designations/<int:pk>/delete',
         views.DesignationDeleteView.as_view(), name='designations-delete'),

    # grouprequiredmixin test
    path('groups/', views.GroupRequiredTestView.as_view(), name='groups-list'),


    # user crud
    path('users/', views.UserListView.as_view(), name='users-list'),
    path('users/create', views.UserCreateView.as_view(), name='users-create'),
    path('users/<int:pk>/update',
         views.UserUpdateView.as_view(), name='users-update'),
    path('users/<int:pk>/status',
         views.UserStatusView.as_view(), name='users-status'),
    path('users/<int:pk>/password-reset',
         views.UserPasswordResetView.as_view(), name='users-password-reset'),

    # todo crud
    path('todo/', views.TodoListView.as_view(), name='todo-list'),
    path('todo/completed/', views.CompletedTaskListView.as_view(),
         name='completed-todo-list'),
    path('todo/important/', views.ImportantTaskListView.as_view(),
         name='important-todo-list'),
    path('todo/missed/', views.MissedTaskListView.as_view(),
         name='missed-todo-list'),
    path('todo/create/', views.TodoCreateView.as_view(), name='todo-create'),
    path('todo/<int:pk>/update/',
         views.TodoUpdateView.as_view(), name='todo-update'),
    path('todo/<int:pk>/detail/',
         views.TodoDetailView.as_view(), name='todo-detail'),
    path('todo/<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),
    path('todo/<int:pk>/manage/', views.ManageTask.as_view(), name='todo-manage'),



]
