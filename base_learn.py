print("hello Python")

my_info = ["code-fusheng", 24, 168.5, True, None]

# 变量
name = "code-fusheng"
age = 24
height = 168.5
is_student = False
score1 = None

# 数据类型 变量不需要声明类型 Python 会自动识别
def test_type():
    print(type(name))  # <class 'str'>
    print(type(age))  # <class 'int'>
    print(type(height))  # <class 'float'>
    print(type(is_student))  # <class 'bool'>
    print(type(score1))  # <class 'NoneType'>
# test_type()

# 运算符
def calculate(n1, n2):
    print("+ : ", n1 + n2)
    print("- : ", n1 - n2)
    print("* : ", n1 * n2)
    print("/ : ", n1 / n2)
    print("//: ", n1 // n2)
    print("% : ", n1 % n2)
    print("**: ", n1 ** n2)
# calculate(1, 2)

# 循环逻辑

# while
def test_while():
    n = 1
    while n <= 5:
        print("while => n : %d" %n)
        n += 1
# test_while()
# for
def test_for():
    for n in range(1, 6):   # range() 函数生成整数集合
        print("for => n : %d" %n)
    str = "code-fusheng"
    for c in str:
        print("for => c : %s" %c)
    obj = ["code-fusheng", 24, 168.5]
    for item in obj:
        print("for => item : ", item)
# test_for()

# Python 内置数据结构

# 列表
def test_list():
    me = ["code-fusheng", 24, 168.5, True, None]
    score = [90, 100, 95, 98]
    name = list("code-fusheng")
    print(name)
# test_list()

# 字典
def test_dict():
    score = {"match": 90, "chinese": 100, "english": 98}
    print(score["chinese"])
    print(score.keys())
    print(score.values())
    print(score.items())
# test_dict()

# 元组
def test_tuple():
    sex1 = ("male", "female")
    sex2 = tuple(["male", "female"])
    for item in sex2:
        print(item)
# test_tuple()

# 函数

# 判断闰年的函数
def is_leap(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 4 == 0 and year % 400 == 0):
        return 1    # 闰年
    else:
        return 0    # 非闰年

# 迭代器
def test_iterator():
    iter1 = iter(my_info)
    print(next(iter1))
# test_iterator()

# yield 生成器 ???

# 类 和 对象

class People:
    def __init__(self, in_name, in_age, in_sex):
        self.name = in_name
        self.age = in_age
        self.sex = in_sex
    def get_name(self):
        return self.name
    def get_info(self):
        print("name:%s, age:%d, sex:%s"%(self.name, self.age, self.sex))

class Student(People):
    def __init__(self, stu_name, stu_age, stu_sex, stu_class):
        People.__init__(self, stu_name, stu_age, stu_sex)   # 初始化父类属性
        self.my_class = stu_class
    def get_info(self):
        print("name:%s, age:%d, sex:%s, class:%s"%(self.name, self.age, self.sex, self.my_class))

# 文件操作
def test_file():
    students = [["code", 1, "X"], ["fusheng", 9, "Y"]]
    # open() 函数用于打开文件
    # > a:表示追加；r:表示只读；w:表示只写
    with open("students.txt", "a", encoding="utf-8") as f:
        for one in students:
            to_str = one[0] + "," + str(one[1]) + "," + one[2] + "\n"
            f.write(to_str)
    student1 = []
    with open("students.txt", "r", encoding="utf-8") as f:
        for one in f:
            one_list = one.strip("\n").split(",")
            one_list[1] = int(one_list[1])
            student1.append(one_list)
    print(student1)
# test_file()

# 异常
def test_except():
    student1 = []
    try:
        with open("students.txt", "r", encoding="utf-8") as f:
            for one in f:
                one_list = one.strip("\n").split(",")
                one_list[1] = int(one_list[1])
                student1.append(one_list)
            print(student1)
    except FileNotFoundError:
        print("文件不存在!")
    except:
        print("其他异常!")
test_except()


if __name__ == "__main__":
    # 类的实例化
    fusheng = People("code-fusheng", 24, "男")
    # print(fusheng.get_name())
    # fusheng.get_info()
    #
    stu = Student("code-fusheng", 21, "男", "软工六班")
    # stu.get_info()








