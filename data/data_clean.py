import pandas as pd
import re

# 构造一个包含问题和答案的数据列表
data = [
    {"question": "How do I make a cake?",
    "answer": "To make a cake, you need flour, sugar, eggs, and butter. Mix them together and bake at 350°F for 30 minutes."},
    {"question": "What is the capital of France?",
    "answer": "The capital of France is Paris."},
    {"question": "How do I change a tire?",
    "answer": "To change a tire, you need a jack and a spare tire. Lift the car with the jack, remove the flat tire, and replace it with the spare."},
]

# 将数据转换为DataFrame格式，方便后续处理
df =  pd.DataFrame(data)

# 步骤1：去除重复数据
# 删除question和answer完全相同的重复行
df = df.drop_duplicates(subset=['question', 'answer'])

# 步骤2：删除包含缺失值的行
df = df.dropna()

# 步骤3：去除无效数据（清理HTML标签、特殊字符等）
# 定义文本清洗函数，根据数据集特点可调整
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r"<[^>]+>", "", text)  # 去除HTML标签
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff,。！？]", " ", text)  # 只保留中英文、数字及部分标点
    return text

# 对question和answer字段分别进行文本清洗
df['question'] = df['question'].apply(clean_text)
df['answer'] = df['answer'].apply(clean_text)

# 打印清洗后的结果
# print(df)


def label_question(question):
    """
    为问题添加标签
    :param question: 问题文本
    :return: 标签
    """
    if pd.isna(question):
        return "general"
    if "cake" in question:
        return "cooking"
    elif "capital" in question:
        return "geography"
    elif "tire" in question:
        return "mechanics"
    else:
        return "general"
    
df['category'] = df['question'].apply(label_question)

def label_answer_length(answer):
    """
    为答案添加标签
    :param answer: 答案文本
    :return: 标签
    """
    if pd.isna(answer):
        return "short"
    length = len(answer)
    if length < 20:
        return "short"
    elif length < 50:
        return "medium"
    else :
        return "long"

df["answer_length"] = df["answer"].apply(label_answer_length)

print(df)

import dask.dataframe as dd

ddf = dd.from_pandas(df, npartitions=2)  # 将 pandas DataFrame 转换为 Dask DataFrame

# 并行应用清洗和标注
ddf['question'] = ddf['question'].map(clean_text, meta=('question', 'str'))
ddf['answer'] = ddf['answer'].map(clean_text, meta=('answer', 'str'))
ddf['category'] = ddf['question'].map(label_question, meta=('category', 'str'))
ddf['answer_length'] = ddf['answer'].map(label_answer_length, meta=('answer_length', 'str'))
# 计算结果
result = ddf.compute()

print(result)