from django.urls import path, include


from .views import DesignationListAPIView

urlpatterns = [
    path("designations/", DesignationListAPIView.as_view(), name="designations-list"),


]