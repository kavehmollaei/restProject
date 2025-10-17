class Car:
    def wheel(self):
        return "I have 4 wheels"
class Plane:
    def wheel(self):
        return "I have 10 wheels"
    def fly(self):
        return "I can fly"


person={"name":"rona","car":"arizo","age":2}

def re_wheels(obj):
    if hasattr(obj,"fly"):
        return obj.fly()
    else:

        return "error"


def re_wheelsNew(obj):
    try:
        return obj.fly()
    except AttributeError:
        return "Error"

a= Car()
b=Plane()
print(re_wheels(a))
print(re_wheels(b))



print(re_wheelsNew(b))
print(re_wheelsNew(a))




