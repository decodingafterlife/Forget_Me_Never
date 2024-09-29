# views.py
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .models import Bookmark
from .serializers import BookmarkSerializer
from .services import generate_bookmark_description
from .pagination import CustomPageNumberPagination

class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated] 

    filter_backends = [filters.SearchFilter]
    search_fields = ['url', 'description']
    throttle_classes = [UserRateThrottle]
    ordering_fields=['url']
    pagination_class = CustomPageNumberPagination

    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

   
    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        
        if not url:
            return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # description = request.data.get('description')

        # if  description is None:
        description = generate_bookmark_description(url)

        data = {
            'url': url,
            'description': description,
            'user': request.user.id
        }

        serializer = self.get_serializer(data=data)
        
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user) 
        
        # Return the serialized data with a 201 response (created)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
