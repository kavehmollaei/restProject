class User:
    username="kaveh"
    userfamily="mollaei"
    userage=39

    def showFullname(self):
        return self.username + self.userfamily
    

a=User()
print(a.showFullname())


def cen_gen(words):
    print("Start...")
    w=None
    while True:
        word = yield w
        if word not in words:
            w=word
        else:
            w="*" * len(word)

g= cen_gen(["khar","gav"])
next(g)
print(g.send("reza"))
print(g.send("gav"))
print(g.send("rgac"))
print(g.send("sahel"))
print(g.send("ali"))
class AreaCalculator:
    def calculate_area(self, shape):
        if isinstance(shape, Rectangle):
            return shape.width * shape.height
        elif isinstance(shape, Circle):
            return 3.14159 * shape.radius * shape.radius
        elif isinstance(shape, Triangle):
            return 0.5 * shape.base * shape.height
        else:
            raise ValueError("Unsupported shape type")

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Circle:
    def __init__(self, radius):
        self.radius = radius

class Triangle:
    def __init__(self, base, height):
        self.base = base
        self.height = height

# Usage
# calculator = AreaCalculator()
# rectangle = Rectangle(5, 10)
# circle = Circle(7)
# print(calculator.calculate_area(rectangle))  # 50
# print(calculator.calculate_area(circle))    # 153.93791
from pprint import pprint
from datetime import datetime
class Product:
    def __init__(self,product_name,price,off) -> None:
        self.product_name=product_name
        self.price = price
        self.off = off

    def __str__(self) -> str:
        return self.product_name
class Comment:
    website_name="test.com"
    def __init__(self,product,name,description,like,dislike) -> None:
        self.product = product
        self.name = name
        self.description = description
        self.date=datetime.now().second
        self.like=like
        self.dislike=dislike
    #Instance method
    def show(self):
        print(f"product: {self.product}\n"
                f"name: {self.name}\n"
                f"description : {self.description}\n"
                f"date: {self.date}\n"
                f"{self.like} and dislike: {self.dislike}\n" 
        )    
    @classmethod
    def info(cls):
        return f"Websitename: {cls.website_name}"
    @classmethod
    def sensorship(cls,product,name,description,like,dislike):
        print("comment was sansor")
        sc= description.replace("tor","*")
        return cls(product,name,sc,like,dislike)
    
    @staticmethod
    def elapsed_time(time):
        pass


    def set_name(self,name):
        self.name = name
    
    def get_name(self):
        return self.name


python_course= Product("python",0,0)
c1= Comment(python_course,"reza","gooooooooooooood",30,10)
c1.show()
print(Comment.info())
c2=Comment.sensorship(python_course,"reza","tor",30,10)
print(c2.show())
print(c1.get_name())