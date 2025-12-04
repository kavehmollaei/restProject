from celery import shared_task
from .models import Article

@shared_task
def notify_subscribers(article_id):
    """
    Simulates sending notifications to subscribers when an article is published
    
    Args:
        article_id (int): The ID of the article to notify about
    """
    try:
        article = Article.objects.get(id=article_id)
        if article.is_published:
            # Simulate sending notifications
            print(f"Sending notifications for article: {article.title}")
            return f"Notifications sent for article {article.title}"
        return "Article is not published yet"
    except Article.DoesNotExist:
        return "Article not found"

@shared_task
def add(x,y):
    return x+y

@shared_task
def send_mail():
    pass