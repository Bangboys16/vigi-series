from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from vigi2.models import Series
from .serializers import SeriesSerializer

@api_view(['GET', 'POST'])
def getRoutes(request): 
    routes = [ 
        'GET /api',
        'GET /api/series',
        'GET /api/series/:id'
    ]
    return Response(routes)

# View for listing all series or creating a new one
@api_view(['GET', 'POST'])
def series_list(request, format=None):
    if request.method == 'GET':
        series = Series.objects.all()
        serializer = SeriesSerializer(series, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SeriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a series by its primary key (pk)
@api_view(['GET', 'PUT', 'DELETE'])
def series_detail(request, pk, format=None):
    try:
        series = Series.objects.get(pk=pk)
    except Series.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = SeriesSerializer(series)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SeriesSerializer(series, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        series.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
