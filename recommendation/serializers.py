from rest_framework import serializers
from .models import Recommendation
from recommendationcrop.models import RecommendationCrop
from recommendationcrop.serializers import RecommendationCropSerializer
from crops.models import Crop  # Import your Crops model

class RecommendationSerializer(serializers.ModelSerializer):
    recommended_crops = RecommendationCropSerializer(many=True,read_only = True)

    class Meta:
        model = Recommendation
        fields = '__all__'


