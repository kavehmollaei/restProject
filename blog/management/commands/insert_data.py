from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models  import User,Profile
from blog.models import Post,Category
import random
from datetime import datetime

category_list=["IT","Design","Fun","Python","Django","PHP"]
class Command(BaseCommand):
    help = "inserting Dummy data"
    def __init__(self, *args, **kwargs):
            super(Command,self).__init__(*args,**kwargs)
            self.fake=Faker()

    def handle(self, *args, **options):
        
        user=User.objects.create(email=self.fake.email(),password="test123!@#")
        profile=Profile.objects.get(user=user)
        print(user,profile)
        profile.first_name=self.fake.first_name()
        profile.last_name=self.fake.last_name()
        profile.description=self.fake.paragraph(nb_sentences=5)
        profile.save()
        for name in category_list:
             Category.objects.get_or_create(name=name)

             
        for _ in range(5):
             Post.objects.create(author=user,image="images/blank.png",title=self.fake.paragraph(nb_sentences=1),content=self.fake.paragraph(nb_sentences=10),status=random.choice([True,False]),category=Category.objects.get(name=random.choice(category_list)),created_date=datetime.now())