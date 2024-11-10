from rest_framework import serializers
from .models import Plant

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = [
            'id', 
            'name', 
            'origin', 
            'lifespan', 
            'weather_conditions', 
            'home_remedies',
            'binomial_name',      # Add binomial_name
            'taxon',              # Add taxon
            'companions',         # Add companions
            'sun_requirements',   # Add sun_requirements
            'growing_degree_days',# Add growing_degree_days
            'sowing_method',      # Add sowing_method
            'spread',             # Add spread
            'row_spacing',        # Add row_spacing
            'height',             # Add height
            'image_url'           # Add image_url
        ]
