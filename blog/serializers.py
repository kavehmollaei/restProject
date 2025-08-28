from rest_framework import serializers
from .models import Post,Category


# class PostSerializer(serializers.Serializer):
#     id= serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
    

class PostSerializer(serializers.ModelSerializer):
    snippet=serializers.CharField(source='get_snippet',read_only=True)
    relative_url=serializers.URLField(source='get_absolute_api_url')
    absolute_url=serializers.SerializerMethodField()
    word_count=serializers.SerializerMethodField(method_name="get_wordCount")
    class Meta:
        model= Post
        fields = ["id",'author','title','content','status','category','relative_url','created_date','snippet','absolute_url','word_count']
        read_only_fields=['content']
    
    def get_absolute_url(self,obj):
        request=self.context.get('request')
        absolute_url=obj.pk
     
        return request.build_absolute_uri(absolute_url)
    
    def get_wordCount(self,obj):
        print(obj.content)
        print(obj.status)
        print(len(obj.content.split()))
        return len(obj.content.split())


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=["id","name"]