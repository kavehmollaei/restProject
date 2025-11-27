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


class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('sci-fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('self-help', 'Self-Help'),
        ('business', 'Business'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fa', 'Persian'),
        ('ar', 'Arabic'),
        ('fr', 'French'),
        ('de', 'German'),
        ('es', 'Spanish'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=300, help_text="The title of the book")
    author = models.CharField(max_length=200, help_text="Author(s) of the book")
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True, 
                           help_text="International Standard Book Number")
    description = models.TextField(blank=True, null=True, 
                                  help_text="Brief description or summary of the book")
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='other',
                            help_text="Genre/category of the book")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en',
                               help_text="Language of the book")
    publisher = models.CharField(max_length=200, blank=True, null=True,
                                help_text="Publisher of the book")
    publication_date = models.DateField(blank=True, null=True,
                                       help_text="Date when the book was published")
    page_count = models.PositiveIntegerField(blank=True, null=True,
                                            help_text="Number of pages in the book")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                               help_text="Price of the book")
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True,
                                   help_text="Cover image of the book")
    is_available = models.BooleanField(default=True,
                                      help_text="Whether the book is currently available")
    stock_quantity = models.PositiveIntegerField(default=0,
                                                help_text="Number of copies available in stock")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['genre']),
            models.Index(fields=['is_available']),
            models.Index(fields=['-created_date']),
        ]
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse('blog:book-detail', kwargs={'pk': self.pk})
    
    @property
    def is_in_stock(self):
        """Check if the book is in stock"""
        return self.stock_quantity > 0 and self.is_available
    
    def reduce_stock(self, quantity=1):
        """Reduce stock quantity by the specified amount"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
            return True
        return False
    
    def add_stock(self, quantity=1):
        """Add stock quantity by the specified amount"""
        self.stock_quantity += quantity
        self.save()