from transformers import pipeline

generate_text = pipeline(
    "text-generation",
    model="deepseek-ai/DeepSeek-V3",  # 替换为实际模型名称
    # trust_remote_code=True,
    # torch_dtype="auto",
    # device_map="auto",
    # max_new_tokens=512,
#    device=0,  # 使用第一个GPU
#    max_length=512,
#    do_sample=True,
#    temperature=0.7,
#    top_k=50,
#    top_p=0.95,
#    num_return_sequences=1,
)

generate_text("In this chapter, we'll discuss first steps with generative AI in Python.")