from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from modelTamrin.models import Article, Category
from django.utils.text import slugify
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Adds 10 sample articles to the database'

    def handle(self, *args, **options):
        User = get_user_model()
        users = User.objects.all()
        categories = Category.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Please create some users first.'))
            return
            
        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please create some categories first.'))
            return

        sample_articles = [
            {
                'title': 'Introduction to Django',
                'content': 'Learn the basics of Django web framework...',
                'is_published': True,
            },
            {
                'title': 'Python Tips and Tricks',
                'content': 'Discover useful Python programming techniques...',
                'is_published': True,
            },
            # ... (8 more sample articles)
        ]

        for i, article_data in enumerate(sample_articles):
            Article.objects.create(
                title=article_data['title'],
                slug=slugify(article_data['title']),
                content=article_data['content'],
                author=users.first(),
                category=categories.first(),
                is_published=article_data['is_published'],
                created_at=datetime.now() - timedelta(days=10-i),
                updated_at=datetime.now() - timedelta(days=10-i)
            )

        self.stdout.write(self.style.SUCCESS('Successfully added 10 sample articles'))
