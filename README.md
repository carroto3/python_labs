# 实验4 - 接口和抽象类（ABC）

## 1. 实验目的

学习和掌握：
- Python中的抽象基类（ABC）
- 接口的概念和使用
- 多态性的实现
- isinstance()的使用

## 2. 接口说明

### 2.1 Printable接口
**作用：** 定义对象可以转换为字符串

**方法：**
- `to_string() -> str`: 返回对象的字符串表示

### 2.2 Comparable接口
**作用：** 定义对象可以相互比较

**方法：**
- `compare_to(other) -> int`: 比较两个对象，返回-1/0/1

## 3. 类的实现

### 3.1 Student（学生类）
- **实现接口：** Printable, Comparable
- **Printable实现：** 显示学生ID、姓名、年龄、成绩
- **Comparable实现：** 按成绩比较

### 3.2 Course（课程类）
- **实现接口：** Printable, Comparable
- **Printable实现：** 显示课程ID、名称、学分、难度
- **Comparable实现：** 按难度等级比较

### 3.3 Book（图书类）
- **实现接口：** Printable
- **Printable实现：** 显示ISBN、书名、作者、页数

## 4. 核心功能

### 4.1 使用接口作为类型
```python
def print_all(items: list[Printable]):
    for item in items:
        print(item.to_string())