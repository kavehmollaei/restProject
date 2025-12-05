from rest_framework import serializers
from .models import Post,Category,Dore


# class PostSerializer(serializers.Serializer):
#     id= serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
    

class CategoryNestedSerializer(serializers.ModelSerializer):
    """Simple nested serializer for Category used in PostSerializer."""
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    snippet=serializers.CharField(source='get_snippet',read_only=True)
    relative_url=serializers.URLField(source='get_absolute_api_url')
    absolute_url=serializers.SerializerMethodField()
    word_count=serializers.SerializerMethodField(method_name="get_wordCount")
    category = CategoryNestedSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model= Post
        fields = ["id",'author','title','content','status','category','category_id','relative_url','created_date','snippet','absolute_url','word_count','updated_date']
        read_only_fields=['content']
    
    def get_absolute_url(self,obj):
        request=self.context.get('request')
        absolute_url=obj.pk
     
        return request.build_absolute_uri(absolute_url)
    
    def get_wordCount(self,obj):
        return len(obj.content.split())


class CategorySerializer(serializers.ModelSerializer):

    family = serializers.SerializerMethodField()
    enable = serializers.BooleanField(default=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'family', 'enable']

class doreModelserializer(serializers.ModelSerializer):
    name=serializers.CharField(required=True,allow_blank=False)
    service = serializers.ChoiceField(choices=["ssh", "web", "ping"])
    updated_date = serializers.DateTimeField(read_only=True)
    class Meta:
        model=Dore
        fields = ["name","time","classCode","teacher","student","service","updated_date"]
    
    def validate_name(self,value):
        return value.lower()

# class AuthorUsernameField(serializers.RelatedField):
#     def to_representation(self, value):
#         print(value)
#         return value.first_name

# Note: PostSerializer is defined above (line 10) with nested category support
# This duplicate definition has been removed to avoid conflicts