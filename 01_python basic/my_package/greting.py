
def print_greeting():
    print("hi")
    
def print_greeting(name):
    return f"{name}, hi"

class Person:
    
    def __init__(self,name,age):
        self.name = name
        self.age=age
        
    def __str__(self):
        return f"name: {self.name}, age: {self.age}"
