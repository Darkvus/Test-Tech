# -*- coding: utf-8 -*-

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


from api.models import Artists, Albums
from api.serializers import ArtistsSerializer, AlbumsSerializer

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
        elif self.action == 'get_all_albums':
            return Albums.objects.all()
        return None
    
    def get_serializer_class(self):
        if self.action == 'get_all_artists':
            return ArtistsSerializer
        elif self.action == 'get_all_albums':
            return AlbumsSerializer
        return super().get_serializer_class()

    def generic_list(self, queryset, pagination=False):
        queryset = self.get_queryset()
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
