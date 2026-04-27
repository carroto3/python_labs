"""
模型类 - 实现接口
"""
from .interfaces import Printable, Comparable


class Student(Printable, Comparable):
    """
    学生类 - 实现了Printable和Comparable两个接口
    """
    
    def __init__(self, student_id: int, name: str, age: int, score: float):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.score = score
    
    # 实现Printable接口
    def to_string(self) -> str:
        return f"学生[ID:{self.student_id}, 姓名:{self.name}, 年龄:{self.age}, 成绩:{self.score}]"
    
    # 实现Comparable接口（按成绩比较）
    def compare_to(self, other) -> int:
        if not isinstance(other, Student):
            raise TypeError("只能与其他学生对象比较")
        
        if self.score < other.score:
            return -1
        elif self.score > other.score:
            return 1
        else:
            return 0


class Course(Printable, Comparable):
    """
    课程类 - 实现了Printable和Comparable两个接口
    """
    
    def __init__(self, course_id: int, name: str, credits: int, difficulty: int):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.difficulty = difficulty  # 难度等级 1-10
    
    # 实现Printable接口
    def to_string(self) -> str:
        return f"课程[ID:{self.course_id}, 名称:{self.name}, 学分:{self.credits}, 难度:{self.difficulty}/10]"
    
    # 实现Comparable接口（按难度比较）
    def compare_to(self, other) -> int:
        if not isinstance(other, Course):
            raise TypeError("只能与其他课程对象比较")
        
        if self.difficulty < other.difficulty:
            return -1
        elif self.difficulty > other.difficulty:
            return 1
        else:
            return 0


class Book(Printable):
    """
    图书类 - 只实现了Printable接口
    """
    
    def __init__(self, isbn: str, title: str, author: str, pages: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.pages = pages
    
    # 实现Printable接口
    def to_string(self) -> str:
        return f"图书[ISBN:{self.isbn}, 书名:{self.title}, 作者:{self.author}, 页数:{self.pages}]"