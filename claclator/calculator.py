from calcs import Calc
all = []

print("select :")
print(" 1, add ")
print("2, minus")
print("3, multi")
print("4, division")

choice = input("enter (1,2,3,4) : ")

x = float(input("enter frist number : "))
y = float(input("enter second number :"))

clac = Calc(x,y)
all.append(clac)

if choice == "1":
    print(f"result : {clac.add()}")
elif choice == "2":
    print(f"result : {clac.minus()}")
elif choice == "3":
    print(f"result : {clac.multi()}")
elif choice == "4":
    print(f"result : {clac.division()}")
else:
    4
    ("invalid input")
