from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from .customevalidators import validate_11_digit_phone
# Create your models here.
User = get_user_model()
#managers
class PostTrueManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)
    

class Post(models.Model):
    STATUS_CHOICES = [
        (True, 'Published'),
        (False, 'Draft'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(choices=STATUS_CHOICES, default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-created_date']
        indexes = [models.Index(fields=['-created_date'])]
    
    objects=models.Manager()
    postmanager=PostTrueManager()
    
    def get_snippet(self):
        return self.content[0:5]
    def get_absolute_api_url(self):
        return reverse('blog:post-detail',kwargs={"pk":self.pk})
    
    def get_abolute_url(self):
        return reverse('blog:mypostdetail',args=[self.id])


    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name

class Dore(models.Model):
    name=models.CharField(max_length=20)
    time=models.IntegerField(validators=[MinValueValidator(0,message='Quantity must be at least 0'),MaxValueValidator(500,message='Quantity must be execed 100')]) 
    teacher=models.ForeignKey(User, on_delete=models.CASCADE)
    classCode=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10)],unique=True)
    def __str__(self):
        return self.name

class Students(models.Model):
    FirstName=models.CharField(max_length=20,blank=False,null=False,db_column='firstName')
    LastName=models.CharField(max_length=20,blank=False,null=False,db_column='lastname')
    Dore=models.ForeignKey('Dore',on_delete=models.CASCADE)
    Address=models.TextField(blank=True,null=True,max_length=200)
    PhoneNumber=models.CharField(max_length=15,validators=[validate_11_digit_phone])
    Email=models.EmailField(null=True,blank=True)
    

    def __str__(self):
        return self.LastName


class Ticket(models.Model):
    message=models.TextField(max_length=500)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.CharField(max_length=11)
    subject=models.CharField(max_length=200)
    def __str__(self):
        return self.subject

class Comment(models.Model):
    post=models.ForeignKey('Post',on_delete=models.CASCADE)
    name= models.CharField(max_length=20,verbose_name="name")
    body= models.TextField(max_length=250)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=False)
    
    class Meta:
        ordering= ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
    

    def __str__(self):
        return f"{self.name}:{self.post}"