from langchain_community.llms.fake import FakeListLLM

fake_llm = FakeListLLM(responses=["Hello"])
fake_llm.invoke("Hi and goodbye, FakeListLLM!")

# responses=[
#         "北京是中国的首都。",
#         "北京位于中国北方，是中国的政治、文化和教育中心。",
#         "北京有许多著名的景点，如故宫、天安门广场和长城。"
#     ]
# fake_llm = FakeListLLM(
#     # 模拟的响应列表
#     responses=[
#         "北京是中国的首都。",
#         "北京位于中国北方，是中国的政治、文化和教育中心。",
#         "北京有许多著名的景点，如故宫、天安门广场和长城。"
#     ],
#     # 模拟的延迟时间（秒）
#     delay=0.5,
#     # 模拟的最大响应长度
#     max_length=100
# )
# # 调用模型生成响应
# response = fake_llm.invoke("In which country is beijing?")
# print(response)
