from rest_framework import serializers

from dashboard.models import Designation

from todoapp.models import Task


class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = ['name', 'position', 'gender', 'date_of_birth']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['user', 'title', 'description',
                  'is_important', 'last_date', 'is_completed', 'is_missed']
