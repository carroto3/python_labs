"""
演示程序 - 展示接口的使用
"""
# 原来的导入（有问题）：
# from .models import Student, Course, Book
# from .interfaces import Printable, Comparable

# 改成绝对导入：
from models import Student, Course, Book
from interfaces import Printable, Comparable


# ============ 通用函数：使用接口作为类型 ============

def print_all(items: list[Printable]):
    """
    通用打印函数 - 接受所有实现了Printable接口的对象
    这是任务4的核心要求：使用接口作为类型
    """
    print("\n" + "="*60)
    print(f"打印 {len(items)} 个对象：")
    print("="*60)
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.to_string()}")
    print("="*60)


def sort_comparable(items: list[Comparable]) -> list[Comparable]:
    """
    通用排序函数 - 接受所有实现了Comparable接口的对象
    """
    # 使用冒泡排序演示
    sorted_items = items.copy()
    n = len(sorted_items)
    
    for i in range(n):
        for j in range(0, n-i-1):
            if sorted_items[j].compare_to(sorted_items[j+1]) > 0:
                sorted_items[j], sorted_items[j+1] = sorted_items[j+1], sorted_items[j]
    
    return sorted_items


def compare_objects(obj1: Comparable, obj2: Comparable):
    """
    比较两个对象并打印结果
    """
    result = obj1.compare_to(obj2)
    
    obj1_str = obj1.to_string() if isinstance(obj1, Printable) else str(obj1)
    obj2_str = obj2.to_string() if isinstance(obj2, Printable) else str(obj2)
    
    if result < 0:
        print(f"\n{obj1_str}\n  小于\n{obj2_str}")
    elif result > 0:
        print(f"\n{obj1_str}\n  大于\n{obj2_str}")
    else:
        print(f"\n{obj1_str}\n  等于\n{obj2_str}")


# ============ 演示场景 ============

def demo_1_printable_interface():
    """
    场景1：演示Printable接口的使用
    """
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + " "*15 + "场景1：Printable接口演示" + " "*18 + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # 创建不同类型的对象
    student = Student(1, "张三", 20, 85.5)
    course = Course(101, "Python程序设计", 4, 7)
    book = Book("978-7-115-12345-6", "Python编程", "李四", 320)
    
    # 使用通用函数print_all - 展示接口作为类型
    all_objects = [student, course, book]
    print_all(all_objects)
    
    # isinstance检查
    print("\n使用isinstance()检查对象是否实现Printable接口：")
    print("-"*60)
    for obj in all_objects:
        class_name = obj.__class__.__name__
        is_printable = isinstance(obj, Printable)
        print(f"{class_name:15} 实现了Printable? {is_printable}")


def demo_2_comparable_interface():
    """
    场景2：演示Comparable接口的使用
    """
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + " "*15 + "场景2：Comparable接口演示" + " "*17 + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # 创建学生对象
    students = [
        Student(1, "张三", 20, 85.5),
        Student(2, "李四", 21, 92.0),
        Student(3, "王五", 19, 78.5),
        Student(4, "赵六", 22, 88.0)
    ]
    
    print("\n原始学生列表：")
    print_all(students)
    
    # 使用通用排序函数
    sorted_students = sort_comparable(students)
    print("\n按成绩排序后：")
    print_all(sorted_students)
    
    # 比较两个学生
    print("\n比较操作：")
    compare_objects(students[0], students[1])


def demo_3_multiple_interfaces():
    """
    场景3：演示多接口实现
    """
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + " "*18 + "场景3：多接口实现" + " "*21 + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # 创建对象
    student = Student(1, "张三", 20, 85.5)
    course = Course(101, "Python程序设计", 4, 7)
    book = Book("978-7-115-12345-6", "Python编程", "李四", 320)
    
    print("\n接口实现情况检查：")
    print("-"*60)
    print(f"{'类名':<15} {'Printable':<15} {'Comparable':<15}")
    print("-"*60)
    
    objects = [
        ("Student", student),
        ("Course", course),
        ("Book", book)
    ]
    
    for class_name, obj in objects:
        is_printable = "✓" if isinstance(obj, Printable) else "✗"
        is_comparable = "✓" if isinstance(obj, Comparable) else "✗"
        print(f"{class_name:<15} {is_printable:<15} {is_comparable:<15}")
    
    print("\n说明：")
    print("• Student和Course实现了两个接口（Printable + Comparable）")
    print("• Book只实现了一个接口（Printable）")


def demo_4_mixed_list():
    """
    场景4：混合列表的处理
    """
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + " "*18 + "场景4：混合列表处理" + " "*19 + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # 创建混合对象列表
    mixed_objects = [
        Student(1, "张三", 20, 85.5),
        Course(101, "Python程序设计", 4, 7),
        Book("978-7-115-12345-6", "Python编程", "李四", 320),
        Student(2, "李四", 21, 92.0),
        Course(102, "数据结构", 4, 9)
    ]
    
    # 所有对象都可以打印（都实现了Printable）
    print("\n所有对象（使用Printable接口）：")
    print_all(mixed_objects)
    
    # 筛选出可比较的对象
    comparable_objects = [obj for obj in mixed_objects if isinstance(obj, Comparable)]
    print(f"\n可比较的对象数量: {len(comparable_objects)}")
    
    # 按类型分组
    students = [obj for obj in comparable_objects if isinstance(obj, Student)]
    courses = [obj for obj in comparable_objects if isinstance(obj, Course)]
    
    if students:
        print("\n学生排序（按成绩）：")
        sorted_students = sort_comparable(students)
        print_all(sorted_students)
    
    if courses:
        print("\n课程排序（按难度）：")
        sorted_courses = sort_comparable(courses)
        print_all(sorted_courses)


# ============ 主函数 ============

def main():
    """
    主函数 - 运行所有演示场景
    """
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + " "*20 + "实验4：接口和抽象类" + " "*19 + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    scenarios = [
        demo_1_printable_interface,
        demo_2_comparable_interface,
        demo_3_multiple_interfaces,
        demo_4_mixed_list
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        scenario()
        if i < len(scenarios):
            input("\n按回车键继续...")
    
    print("\n" + "="*60)
    print("演示完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()