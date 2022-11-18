# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


from api.models import Artists, Albums, Tracks
from api.serializers import (
    ArtistsSerializer, AlbumsSerializer, DataAlbumsSerializer, 
    TracksSerializer
)

class ApiViewSet(GenericViewSet):
    """
    Base class for all API
    """

    """
        ● Dado un músico / grupo, obtener un listado de todos sus discos.
        ● Dado un disco, obtener un listado de todas las canciones.
        ● Listado de todos los discos con los siguientes datos agregados:
            ○ Nombre del músico / grupo.
            ○ Número total de canciones.
    """

    def get_queryset(self):
        if self.action == 'get_all_artists':
            return Artists.objects.all()
        elif self.action in ['get_all_albums', 'get_all_albums_with_data']:
            return Albums.objects.all()
        elif self.action == 'get_tracks_by_album_id':
            return Tracks.objects.filter(albumid=self.kwargs['album_id'])
        elif self.action == "get_tracks_by_album_name":
            return Tracks.objects.filter(albumid__title=self.kwargs['album_name'])
        elif self.action == 'get_albums_by_artist_id':
            return Albums.objects.filter(artistid=self.kwargs['artist_id'])
        elif self.action == "get_albums_by_artist_name":
            return Albums.objects.filter(artistid__name=self.kwargs['artist_name'])
        return None

    def get_serializer_class(self):
        if self.action == 'get_all_artists':
            return ArtistsSerializer
        elif self.action in ['get_all_albums', 'get_albums_by_artist_id', 'get_albums_by_artist_name']:
            return AlbumsSerializer
        elif self.action == 'get_all_albums_with_data':
            return DataAlbumsSerializer
        elif self.action in ['get_tracks_by_album_id', 'get_tracks_by_album_name']:
            return TracksSerializer
        return super().get_serializer_class()

    def generic_list(self, queryset, pagination=False):
        page = self.paginate_queryset(queryset)
        data = {}
        if page is not None and pagination:
            return self.get_paginated_response( self.get_serializer(page, many=True).data)
        else:
            data = self.get_serializer(queryset, many=True).data
        return Response(data)
    
    @extend_schema(
        parameters=[
          OpenApiParameter(name="pagination", type=OpenApiTypes.BOOL, location=OpenApiParameter.QUERY, required=False, description="Filtro de paginacion"),
        ],
    )    
    @action(detail=False, methods=['get'], url_path='all-artists')
    def get_all_artists(self, request, *args, **kwargs):
        pagination = True if self.request.query_params.get('pagination', "false") == "true" else False
        return self.generic_list(self.get_queryset(), pagination)

    @extend_schema(
        parameters=[
          OpenApiParameter(name="pagination", type=OpenApiTypes.BOOL, location=OpenApiParameter.QUERY, required=False, description="Filtro de paginacion"),
        ],
    )    
    @action(detail=False, methods=['get'], url_path='all-albums')
    def get_all_albums(self, request, *args, **kwargs):
        pagination = True if self.request.query_params.get('pagination', "false") == "true" else False
        return self.generic_list(self.get_queryset(), pagination)
    
    @extend_schema(
        parameters=[
          OpenApiParameter(name="pagination", type=OpenApiTypes.BOOL, location=OpenApiParameter.QUERY, required=False, description="Filtro de paginacion"),
        ],
    )
    @action(detail=False, methods=['get'], url_path='data-albums')
    def get_all_albums_with_data(self, request, *args, **kwargs):
        pagination = True if self.request.query_params.get('pagination', "false") == "true" else False
        return self.generic_list(
            self.get_queryset().annotate(
                total_tracks=Count('tracks')
            ), 
            pagination
        )
    
    @extend_schema(
        parameters=[
          OpenApiParameter(name="album_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True, description="Album ID"),
        ],
    )
    @action(detail=False, methods=['get'], url_path='tracks-by-albums-id/(?P<album_id>[^/.]+)')
    def get_tracks_by_album_id(self, request, album_id, *args, **kwargs):
        qs = self.get_queryset()
        return Response(self.get_serializer(qs, many=True).data)
    
    @action(detail=False, methods=['get'], url_path='tracks-by-albums/(?P<album_name>[^/.]+)')
    def get_tracks_by_album_name(self, request, album_name, *args, **kwargs):
        qs = self.get_queryset()
        return Response(self.get_serializer(qs, many=True).data)
    
    @extend_schema(
        parameters=[
          OpenApiParameter(name="artist_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True, description="Artist ID"),
        ],
    )
    @action(detail=False, methods=['get'], url_path='albums-by-artist-id/(?P<artist_id>[^/.]+)')
    def get_albums_by_artist_id(self, request, artist_id, *args, **kwargs):
        qs = self.get_queryset()
        return Response(self.get_serializer(qs, many=True).data)
    
    @action(detail=False, methods=['get'], url_path='albums-by-artist/(?P<artist_name>[^/.]+)')
    def get_albums_by_artist_name(self, request, artist_name, *args, **kwargs):
        qs = self.get_queryset()
        return Response(self.get_serializer(qs, many=True).data)

