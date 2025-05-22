import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # 关闭tokenizers并行警告

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from torch.utils.data import Dataset

# 指定模型名称
# - **GPT 系列**  
#   - gpt2-medium  
#   - gpt2-large  
#   - gpt2-xl  
#   - distilgpt2（更小更快）

# - **OpenAI GPT**  
#   - openai-gpt

# - **BLOOM 系列**  
#   - bigscience/bloom-560m  
#   - bigscience/bloomz-560m

# - **Llama 系列**（需手动下载权重）  
#   - meta-llama/Llama-2-7b-hf  
#   - meta-llama/Llama-2-13b-hf

# - **MPT 系列**  
#   - mosaicml/mpt-7b-storywriter

# - **Falcon 系列**  
#   - tiiuae/falcon-7b

# - **Qwen 系列**  
#   - Qwen/Qwen-7B-Chat

# - **Chinese GPT**  
#   - IDEA-CCNL/Wenzhong-GPT2-110M  
#   - THUDM/chatglm2-6b

# - **其他**  
#   - EleutherAI/gpt-neo-125M  
#   - EleutherAI/gpt-j-6B  
#   - EleutherAI/gpt-neox-20b

model_name = "bigscience/bloom-560m"  # 或其他模型名称
# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(model_name)
# 修复：为tokenizer设置pad_token（GPT2默认没有pad_token）
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
# 加载预训练模型
model = AutoModelForCausalLM.from_pretrained(model_name)

# 构造训练数据
medical_data = [
    {"input": "What is the capital of France? The capital of France is Pairs."},
    {"input": "What is the largest mammal? The largest mammal is the blue whale."},
]

# 数据预处理函数，将文本转为模型输入格式
def prepare_data(data):
    inputs = tokenizer([item["input"] for item in data], return_tensors="pt", padding=True, truncation=True)
    labels = inputs.input_ids.clone()  # 标签与输入一致（自回归训练）
    return {"input_ids": inputs.input_ids, "attention_mask": inputs.attention_mask, "labels": labels}

# 处理后的数据
processed_data = prepare_data(medical_data)

# 自定义Dataset类，适配Trainer
class MedicalDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data["input_ids"])

    def __getitem__(self, idx):
        return {key: self.data[key][idx] for key in self.data.keys()}

# 构建训练集
train_dataset = MedicalDataset(processed_data)

# 训练参数设置
training_args = TrainingArguments(
    output_dir="./results",             # 输出目录
    num_train_epochs=3,                 # 训练轮数
    per_device_train_batch_size=2,      # 每个设备的batch大小
    save_steps=10000,                   # 保存步数
    save_total_limit=2,                 # 最多保存模型数
    logging_dir='./logs',               # 日志目录
)

# 构建Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)
# 开始训练
trainer.train()

# 推理/生成函数
def generate_response(prompt, model, tokenizer, max_length=50):
    # 编码输入，同时获取 attention_mask
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    # 明确指定 pad_token_id
    pad_token_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],  # 传递 attention_mask
        max_length=max_length,
        num_return_sequences=1,
        pad_token_id=pad_token_id
    )
    # 解码输出
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 示例推理
prompt = "What is the capital of France?"
response = generate_response(prompt, model, tokenizer)
print(response)