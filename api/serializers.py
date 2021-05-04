from rest_framework import serializers

from dashboard.models import Designation

class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = ['name', 'position', 'gender', 'date_of_birth']




