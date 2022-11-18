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


class DataAlbumsSerializer(serializers.ModelSerializer):
    num_tracks = serializers.SerializerMethodField()
    artistid = ArtistsSerializer()
    total_tracks = serializers.IntegerField()
    
    class Meta:
        model = Albums
        fields = [
            'title', 
            'num_tracks', 
            'artistid',
            'total_tracks',
        ]
    
    def get_num_tracks(self, obj):
        return obj.tracks_set.count()
