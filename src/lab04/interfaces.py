"""
接口定义模块 - 使用ABC（抽象基类）
"""
from abc import ABC, abstractmethod


class Printable(ABC):
    """
    可打印接口 - 要求实现字符串表示方法
    """
    
    @abstractmethod
    def to_string(self) -> str:
        """返回对象的字符串表示"""
        pass


class Comparable(ABC):
    """
    可比较接口 - 要求实现比较方法
    """
    
    @abstractmethod
    def compare_to(self, other) -> int:
        """
        比较两个对象
        返回值：
            -1: 当前对象小于other
             0: 相等
             1: 当前对象大于other
        """
        pass