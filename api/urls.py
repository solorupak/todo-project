from django.urls import path, include


from .views import DesignationListAPIView, TaskListCreateApiView, TaskUpdateDeleteApiView

urlpatterns = [
    path("designations/", DesignationListAPIView.as_view(),
         name="designations-list"),
    path("tasks/", TaskListCreateApiView.as_view(), name="tasks-list-create"),
    path("tasks/<int:pk>/", TaskUpdateDeleteApiView.as_view(),
         name="tasks-update-delete"),


]
