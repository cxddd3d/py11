class Parent(object):
    x = 1

class Child1(Parent):
    pass

class Child2(Parent):
    pass

print(Parent.x, Child1.x, Child2.x) #1 1 1
Child1.x = 2
print(Parent.x, Child1.x, Child2.x) #1 2 1
Parent.x = 3
print(Parent.x, Child1.x, Child2.x) #3 2 3

p=Parent()
c1=Child1()
c2=Child2()

print(p.x,c1.x,c2.x) #3 2 3
c1.x=4
print(p.x,c1.x,c2.x,Child1.x) #3 4 3 2
p.x=5
print(p.x,c1.x,c2.x)  #5 4 3

#对象属性查找顺序，对象属性---》类属性--》父类属性