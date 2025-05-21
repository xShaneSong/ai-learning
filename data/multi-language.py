from transformers import AutoTokenizer

# 加载支持多语言的预训练模型的分词器
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

# 定义多语言文本
texts = [
    "Hello, how are you?",  # English
    "Bonjour, comment ça va?",  # French
    "Hola, ¿cómo estás?",  # Spanish
    "你好，你好吗？",  # Chinese
    "こんにちは、お元気ですか？"  # Japanese
]

# 编码文本
encoded = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
print(encoded)
print("-----------")

# 解码，验证结果
decoded = [tokenizer.decode(ids, skip_special_tokens=True) for ids in encoded["input_ids"]]
print("Encoded IDs:", encoded["input_ids"])
print("-----------")
print("Decoded Texts:", decoded)
print("-----------")
for line in decoded:
    print(line)