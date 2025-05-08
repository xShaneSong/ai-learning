# markdown file
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader
)
from langchain_core.documents import Document

markdown_path = "../README.md"
loader = UnstructuredMarkdownLoader(markdown_path)

data = loader.load()
assert len(data) == 1
assert isinstance(data[0], Document)
readme_content = data[0].page_content
print(data)

# for document in data[:]:
#     print(f"{document}\n")

# CSV file
from langchain_community.document_loaders import (
    UnstructuredCSVLoader
)
from langchain_core.documents import Document
loader = UnstructuredCSVLoader(
    file_path="./test.csv",
    csv_args={"delimiter": ","}
)

data = loader.load()
print(data)
# for record in data[:]:
#     print(record)

# CSV string data
import tempfile
from io import StringIO

string_data = """
"Team", "Payroll (millions)", "Wins"
"Nationals",     81.34, 98
"Reds",          82.20, 97
"Yankees",      197.96, 95
"Giants",       117.62, 94
""".strip()


with tempfile.NamedTemporaryFile(delete=False, mode="w+") as temp_file:
    temp_file.write(string_data)
    temp_file_path = temp_file.name

loader = UnstructuredCSVLoader(file_path=temp_file_path)
data = loader.load()
for record in data[:]:
    print(record)

# Directory loader
from langchain_community.document_loaders import DirectoryLoader, PythonLoader
# text_loader_kwargs = {"autodetect_encoding": False}
text_loader_kwargs = {}
loader1 = DirectoryLoader("../", glob="**/*.py",
                          show_progress=True,
                          use_multithreading=True,
                          loader_cls=PythonLoader,
                          silent_errors=True,
                          loader_kwargs=text_loader_kwargs)
docs = loader1.load()
print(len(docs))
# for doc in docs[:]:
    # print(f"{doc}\n")

# JSON file
from langchain_community.document_loaders import JSONLoader
import json
from pathlib import Path
from pprint import pprint

file_path='./test.json'
data = json.loads(Path(file_path).read_text())
pprint(data)

loader = JSONLoader(
    file_path='./test.json',
    jq_schema='.messages[].content',
    # text_content=False,
    # json_lines=True,
    # content_key=".content",
    # is_content_key_jq_parsable=True,
    )

data = loader.load()
pprint(data)