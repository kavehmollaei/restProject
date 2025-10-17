from re import search
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView,RedirectView
from ..models import Post,Category
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
#REST Framework imports commented out until package is installed
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import PostSerializer,CategorySerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,mixins,ListAPIView,ListCreateAPIView
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter
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
class CategoryModelViewSet(viewsets.ModelViewSet):
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

class CategoryListAPIView(APIView):
    """API view for listing and creating categories."""
    serializer_class = CategorySerializer

    def get(self, request):
        """Retrieve all categories."""
        categories = Category.objects.all()  # type: ignore
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new category."""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
