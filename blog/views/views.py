from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView,RedirectView
from ..models import Post,Category
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import PostSerializer,CategorySerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,mixins,ListAPIView,ListCreateAPIView
from rest_framework import viewsets
# Create your views here.







def RedirectFunc(request):
    return redirect('https://maktabkhooneh.com')




def IndexView(request):
    '''
    function base view
    '''
    context={"name":"kaveh"}
    return render(request,'index.html',context=context)

class IndexViewclass(TemplateView):
    template_name="home.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["name"]="Ronamollaei"
        context['posts'] =  Post.objects.all()
        return context



class RedirectToMaktab(RedirectView):
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
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data)        

class PostDetail(APIView):
    serializer_class=PostSerializer
    def get(self,request,id):
        post=get_object_or_404(Post,pk=id,status=True)
        serilaizer=PostSerializer(instance=post)
        return Response(serilaizer.data)
    def put(self,request,id):
        post=get_object_or_404(Post,pk=id)
        serializer=PostSerializer(instance=post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
    def delete(self,request,id):
        post=get_object_or_404(Post,pk=id)
        post.delete()
        return Response({"details":"item removed successfully"},status=status.HTTP_204_NO_CONTENT)

# class PostList(GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
#     serializer_class = PostSerializer
#     queryset=Post.objects.all()
    
#     def get(self,request,*args,**kwargs):
#         print(args)
#         print(kwargs)
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

class PostList(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset=Post.objects.all()

    

    # def get(self,request):
    #     queryset=self.get_queryset()
    #     serializer=PostSerializer(instance=queryset,many=True)
    #     return Response(serializer.data)
        
    

class PostDetail(GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class=PostSerializer
    queryset=Post.objects.filter()
    lookup_field='id'
    def get(self,request,*args,**kwargs):
        print(request)
        return self.retrieve(request,*args,**kwargs)
    def put(self,requset,*args,**kwargs):
        return self.update(requset,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
    
class PostViewSet(viewsets.ViewSet):
    serializer_class=PostSerializer
    queryset=Post.objects.all()

    def list(self,request):
        serializer=PostSerializer(instance=self.queryset,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,id=None):
        post_object=get_object_or_404(Post,pk=id)
        serializer=PostSerializer(instance=post_object)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class=PostSerializer
    queryset=Post.objects.all()


class CategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


