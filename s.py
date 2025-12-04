# names=['kaveh','kevien','mark','noora','jack','rona']
# first,*middle,last=names
# print(first)
# def show(name):
#     if name=="rona":
#         return True

# print(list(filter(show,names)))

dict_sample={"name": "Ali", "grade": 85, "age": 20}
# print(dict_sample.get("dd"))
s="family"


class mydict(dict):
    def __missing__(self,key):
        print("not exist")
        if isinstance(key, str):
            self[key] = key * 2
            return self[key]
        elif isinstance(key,int):
            return self
        return

new_dict=mydict(dict_sample)
print(new_dict[1])


# lst=[item for item in range(101)]

# print(list(filter(lambda x: x %2 == 0,lst)))

# words = ["hello", "", "world", "", "python", " "]

# non_empty = list(filter(lambda x: x.strip() != "", words))
# print(non_empty)


# students = [
#     {"name": "Ali", "grade": 85, "age": 20},
#     {"name": "Maryam", "grade": 92, "age": 19},
#     {"name": "Reza", "grade": 78, "age": 21},
#     {"name": "Sara", "grade": 95, "age": 18},
#     {"name": "Amir", "grade": 65, "age": 22}
# ]

# print(list(filter(lambda x : x["grade"]> 80,students)))
# print(list(filter(lambda x: x["age"] > 10 and x["grade"] >=90 ,students)))

# matrix = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9],
#     [10, 11, 12]
# ]


# print(list(filter(lambda x: sum(x) > 15 ,matrix)))
# while (line :=input("Enter text: ")) != "exit":
#     print(f"You entered: {line}")
#     line = input("Enter text: ")
