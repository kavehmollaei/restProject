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
        return len(obj.content.split())


class CategorySerializer(serializers.ModelSerializer):

    family = serializers.SerializerMethodField()
    enable = serializers.BooleanField(default=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'family', 'enable']
    

    def validate_name(self, value):
        if value == "test":
            raise serializers.ValidationError("Name cannot be test")
        print(value)

        return super().validate(value)
    def validate_enable(self, value):
        print(value)
        if value == "false":

            raise serializers.ValidationError(f"Name cannot be {value}")
        return super().validate(value)
    
    def create(self, validated_data):
        label = validated_data.pop('enable', None)
        instance = super().create(validated_data)
        if label:
            # instance.enable = datetime.date.today()
            instance.save()
        return instance
    def get_family(self, obj):
        print(obj)
        return f"family is {obj.name}"
    
    def  to_representation(self, instance):
        data = super().to_representation(instance)
        # method=self.context.get("view").action
        method_instance=self.context.get("view")
        method=getattr(method_instance,"action",None)
        # print(getattr(view,"action",None))
        if method == "retrieve":
            data['name'] = instance.name.upper()
            data["mac"] = "add"
            return data
        return data

# class AuthorUsernameField(serializers.RelatedField):
#     def to_representation(self, value):
#         print(value)
#         return value.first_name
class PostSerializer(serializers.Serializer):
    # author=AuthorUsernameField(read_only=True)
    author=serializers.CharField(source="author.id")
    author = serializers.SerializerMethodField()
    title=serializers.CharField()
    content=serializers.CharField()
    status=serializers.BooleanField()
    category=serializers.CharField()
    created_date=serializers.DateTimeField()
    updated_date=serializers.DateTimeField()
    class Meta:
        model=Post
        fields=["id","author","title","content","status","category","created_date","updated_date"]

    def get_author(self,obj):
        return {" author": obj.author.email

        }