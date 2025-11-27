from re import search
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView,RedirectView
from ..models import Post,Category
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
#REST Framework imports commented out until package is installed
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from ..serializers import PostSerializer,CategorySerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,mixins,ListAPIView,ListCreateAPIView
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
#Create your views here.







def RedirectFunc(request):
    return redirect('https://maktabkhooneh.com')




def IndexView(request):
    '''
    function base view
    '''
    context={"name":"kaveh"}
    return render(request,'index.html',context=context)

class IndexViewclass(TemplateView):
    """Class-based view for the home page."""
    template_name="home.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["name"]="Ronamollaei"
        context['posts'] =  Post.objects.all()
        return context



class RedirectToMaktab(RedirectView):
    """Redirect view to Maktabkhooneh website."""
    permanent = False
    url="https://maktabkhooneh.com"
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Post,pk=kwargs['pk'])
        print(obj)
        param={'name':obj}
        
        return super().get_redirect_url(param,*args, **kwargs)

data= {
    'id':1,
    'title':'Hello'
}


def api_post_list_view(request):
    return HttpResponse("ok")



@api_view(['GET'])
def apitestresponse(request):
    obj=Post.objects.all()
    context={'name':'rona','test':request.query_params}
    headers={"X-Custom-Header": "dfdf"}
    return Response(data=context,status=202,headers=headers)

@api_view(['GET','PUT','DELETE'])
def postdetail(request,id):
    post=get_object_or_404(Post,pk=id)
    if request.method == "GET":
        serializer=PostSerializer(instance=post)
        return Response(data=serializer.data)
    elif request.method == "PUT":
        serializer=PostSerializer(instance=post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        post.delete()
        return Response({"detail":"item removed successfully"},status=status.HTTP_204_NO_CONTENT)
        
    
    
    # try:        
    #     post=Post.objects.get(pk=id)
    #     serializer=PostSerializer(post)
    #     return Response(data=serializer.data)
    # except Post.DoesNotExist:
    #     return Response( data="Ffgfgf",status=status.HTTP_404_NOT_FOUND)
            

# @api_view(['GET','POST'])
# def postList(request):
#     print(request.data)
#     print(type(request.data))
#     if request.method == "GET":
#         posts=Post.objects.all()
#         serializer=PostSerializer(posts,many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer=PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             print(serializer.data)
#             return Response(serializer.data)
#         else:
#             return Response(data=serializer.errors)        
    
class PostList(ListCreateAPIView):
    """API view for listing and creating posts."""
    serializer_class = PostSerializer
    queryset=Post.objects.all()

class PostViewSet(viewsets.ModelViewSet):
    """ModelViewSet for Post CRUD operations."""
    serializer_class=PostSerializer
    queryset=Post.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'title', 'created_date', 'updated_date']
    ordering = ['-created_date']  # default ordering by newest first
    search_fields = ['title', 'content']
    filterset_fields = ['status', 'category', 'author']
    def list(self, request, *args, **kwargs):
        print("Rona")
        return super().list(request, *args, **kwargs)
class CategoryModelViewSert(viewsets.ModelViewSet):
    """ModelViewSet for Category CRUD operations."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()  # type: ignore
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'name']
    ordering = ['id']  # default ordering
    search_fields = ['^name']
    
    def list(self, request, *args, **kwargs):
        """Override list method to add custom logging."""
        return super().list(request, *args, **kwargs)


class CategoryModelViewSet(viewsets.ModelViewSet):
    """ModelViewSet for Category CRUD operations."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()  # type: ignore

    def list(self, request, *args, **kwargs):
        print("Rona")
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        print("Rona")
        instance = self.get_object()
        serializer= self.get_serializer(instance,)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        
        print(request.data)  # use request.data directly from the parsed request
        
        return super().create(request, *args, **kwargs)


class CategoryListAPIView(APIView):
    """API view for listing and creating categories."""
    # serializer_class = CategorySerializer

    def get(self, request):
        """Retrieve all categories."""
        # categories = Category.objects.all().values('id', 'name').first()  # type: ignore
        categiries=Category.objects.all()
        serializer = CategorySerializer(categiries,many=True)
        return Response(data=serializer.data)

    def post(self, request):
        """Create a new category."""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ============================================================================
# VIEWSET EXAMPLES
# ============================================================================

# Example 1: ModelViewSet - Provides full CRUD operations (list, create, retrieve, update, destroy)
# Automatically provides: list(), create(), retrieve(), update(), partial_update(), destroy()
class CategoryViewSetExample(viewsets.ModelViewSet):
    """
    ModelViewSet example - Full CRUD operations.
    
    Endpoints automatically created:
    - GET /categories/          -> list() - Get all categories
    - POST /categories/         -> create() - Create new category
    - GET /categories/{id}/     -> retrieve() - Get single category
    - PUT /categories/{id}/      -> update() - Full update
    - PATCH /categories/{id}/   -> partial_update() - Partial update
    - DELETE /categories/{id}/  -> destroy() - Delete category
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # Optional: Add permissions
    
    # Optional: Add filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name', 'enable']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['id']
    
    # Override methods for custom behavior
    def list(self, request, *args, **kwargs):
        """Custom list behavior - called on GET /categories/"""
        # Add custom logic here
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Custom create behavior - called on POST /categories/"""
        # Add custom logic here (e.g., logging, validation)
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Custom retrieve behavior - called on GET /categories/{id}/"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Custom update behavior - called on PUT /categories/{id}/"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Custom destroy behavior - called on DELETE /categories/{id}/"""
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Example 2: ReadOnlyModelViewSet - Provides only read operations (list, retrieve)
class CategoryReadOnlyViewSetExample(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet example - Read-only operations.
    
    Endpoints automatically created:
    - GET /categories/          -> list() - Get all categories
    - GET /categories/{id}/     -> retrieve() - Get single category
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'name']


# Example 3: ViewSet - Base class, requires you to implement all actions manually
class CategoryCustomViewSet(viewsets.ViewSet):
    """
    ViewSet example - Manual implementation of all actions.
    More flexible but requires more code.
    
    You need to manually define all actions you want.
    """
    def list(self, request):
        """GET /categories/"""
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """GET /categories/{pk}/"""
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def create(self, request):
        """POST /categories/"""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """PUT /categories/{pk}/"""
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        """PATCH /categories/{pk}/"""
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """DELETE /categories/{pk}/"""
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Example 4: GenericViewSet - Mix of generic views with custom actions
class CategoryGenericViewSet(viewsets.GenericViewSet):
    """
    GenericViewSet example - Use mixins for common operations.
    More control than ModelViewSet, less code than ViewSet.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    # Use mixins to add specific actions
    # from rest_framework import mixins
    # class CategoryGenericViewSet(mixins.ListModelMixin,
    #                              mixins.CreateModelMixin,
    #                              mixins.RetrieveModelMixin,
    #                              viewsets.GenericViewSet):
    #     ...
    
    def list(self, request, *args, **kwargs):
        """GET /categories/"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """POST /categories/"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Example 5: ModelViewSet with custom actions using @action decorator
class CategoryViewSetWithCustomActions(viewsets.ModelViewSet):
    """
    ModelViewSet with custom actions example.
    
    Standard CRUD + custom endpoints:
    - GET /categories/{id}/enable/     -> enable_category()
    - POST /categories/{id}/disable/  -> disable_category()
    - GET /categories/active/         -> get_active_categories()
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    # Custom action - GET /categories/{id}/enable/
    @action(detail=True, methods=['get'])
    def enable(self, request, pk=None):
        """Enable a category."""
        category = self.get_object()
        category.enable = True
        category.save()
        serializer = self.get_serializer(category)
        return Response(serializer.data)
    
    # Custom action - POST /categories/{id}/disable/
    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        """Disable a category."""
        category = self.get_object()
        category.enable = False
        category.save()
        serializer = self.get_serializer(category)
        return Response(serializer.data)
    
    # Custom action - GET /categories/active/ (detail=False means list action)
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active categories."""
        active_categories = Category.objects.filter(enable=True)
        serializer = self.get_serializer(active_categories, many=True)
        return Response(serializer.data)
    
    # Custom action with custom URL path
    @action(detail=False, methods=['get'], url_path='custom-path')
    def custom_action(self, request):
        """Custom action with custom URL path."""
        return Response({"message": "This is a custom action"})
