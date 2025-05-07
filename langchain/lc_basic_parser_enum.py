from langchain.output_parsers.enum import EnumOutputParser
from enum import Enum

class Colors(Enum):
    RED = "红色"
    GREEN = "绿色"
    BLUE = "蓝色"
    YELLOW = "黄色"


# 初始化输出解析器
output_parser = EnumOutputParser(Colors)
print(output_parser.parse("红色"))
