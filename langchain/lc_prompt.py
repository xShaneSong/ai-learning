from langchain.prompts import PipelinePromptTemplate, PromptTemplate

full_template = """{introduction}
{example}
{start}"""

full_prompt = PromptTemplate.from_template(full_template)
introduction_template = """你在模仿{person}。"""
introduction_prompt = PromptTemplate.from_template(introduction_template)

example_template = """下面是一个交互的例子：
Q:{example_q}
A:{example_a}"""
example_prompt = PromptTemplate.from_template(example_template)

start_template = """现在，真的这么做!
Q:{input}
A:"""
start_prompt = PromptTemplate.from_template(start_template)

input_prompts = [
    ("introduction", introduction_prompt),
    ("example", example_prompt),
    ("start", start_prompt),
]

pipeline_prompt = PipelinePromptTemplate(
    final_prompt=full_prompt,
    pipeline_prompts=input_prompts)
pipeline_prompt.input_variables = ["example_a", "person","example_q", "input"]
print(pipeline_prompt.format(
    example_a="我喜欢吃苹果。",
    person="小明",
    example_q="你喜欢吃什么？",
    input="你喜欢吃什么水果？"
))