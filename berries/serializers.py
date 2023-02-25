# berries/serializers.py

from rest_framework import serializers


class BerryStatsSerializer(serializers.Serializer):
    berries_names = serializers.ListField(child=serializers.CharField())
    min_growth_time = serializers.IntegerField()
    max_growth_time = serializers.IntegerField()
    median_growth_time = serializers.FloatField()
    mean_growth_time = serializers.FloatField()
    variance_growth_time = serializers.FloatField()
    frequency_growth_time = serializers.DictField(child=serializers.IntegerField())
