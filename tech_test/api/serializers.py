# -*- coding: utf-8 -*-

from rest_framework import serializers

from api.models import Artists, Tracks, Albums


class ArtistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists
        fields = [
            'name',
        ]

class TracksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tracks
        fields = [
            'name', 
            'milliseconds', 
        ]

class AlbumsSerializer(serializers.ModelSerializer):
    tracks_set = TracksSerializer(many=True)
    
    class Meta:
        model = Albums
        fields = [
            'title', 
            'tracks_set', 
        ]
