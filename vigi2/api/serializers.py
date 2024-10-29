from rest_framework.serializers import ModelSerializer
from vigi2.models import Series


class SeriesSerializer(ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'