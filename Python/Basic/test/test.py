class Parent():
    def __init__(self, name):
        self.name = name
        print("Parent")
        print(name)

class Child(Parent):
    def __init__(self, age, name):
        super().__init__(name)
        self.age = age
        print("Child")
        print(self.age)
        print(self.name)
        
        
if __name__ == "__main__":
    Child(1,"sb")
