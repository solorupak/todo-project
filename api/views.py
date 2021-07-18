
from rest_framework import serializers
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from dashboard.models import Designation
from todoapp.models import Task
from .mypaginations import MyCursorPagination
from .serializers import DesignationSerializer, TaskSerializer


class DesignationListAPIView(ListAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    pagination_class = MyCursorPagination

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class TaskListCreateApiView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = MyCursorPagination

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class TaskUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
