from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from ..models import Post,Ticket,Comment
from django.core.paginator import Paginator
from django.views.generic import ListView,DetailView
from blog.forms.forms import TicketForm
from django.views.decorators.http import  require_POST



def index(request):

    return render(request,template_name='blog/index.html')

# def mypostList(request):
#     posts=Post.objects.all()
#     paginator=Paginator(posts,5)
#     page_number=request.GET.get('page',1)
#     print(request.GET)
#     print(request.method)
#     posts=paginator.page(page_number)
#     print(posts.has_previous())
#     context={'posts':posts,
#              }
#     # print(context)
#     return render(request,template_name='blog/list.html',context=context)


class PostListView(ListView):
    queryset=Post.postmanager.all()
    paginate_by=3
    context_object_name="posts"
    template_name='blog/list.html'


def mypostdetail(request,id):
    try:
        post=Post.postmanager.get(id=id)
    except:
        raise Http404("No Post Found")
    
    context={'post':post}
    return render(request,template_name='blog/details.html',context=context)


class mypostdetailview(DetailView):
    model = Post
    template_name='blog/details.html'


def ticket(request):
    if request.method == "POST":
        form=TicketForm(request.POST)
        print(request.POST)
        if form.is_valid():
            ticket_obj=Ticket.objects.create()
            clean_data=form.cleaned_data
            ticket_obj.message=clean_data["message"]
            ticket_obj.name=clean_data['name']
            ticket_obj.email=clean_data['email']
            ticket_obj.phone=clean_data['phone']
            ticket_obj.subject=clean_data['subject']
            ticket_obj.save()
            return redirect('blog:index')
    else:
        form=TicketForm()
        print(TicketForm)
    return render(request,template_name="forms/ticket.html",context={'form':form})


@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Comment,id=post_id)
    comment= None
    form=CommentForms(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context={"post":post,'form':form,'comment':comment}
    return render(request,'forms/comment.html',context=context)



