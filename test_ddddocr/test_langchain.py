import os
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
# from langchain import OpenAI
from langchain_openai import AzureOpenAI,OpenAIEmbeddings,AzureOpenAIEmbeddings


# from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
# from langchain_community.document_loaders.larksuite import (
#     LarkSuiteDocLoader,
#     LarkSuiteWikiLoader,
# )
os.environ["OPENAI_API_VERSION"] = "2023-12-01-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://models.inference.ai.azure.com"
os.environ["AZURE_OPENAI_API_KEY"] = os.environ["GITHUB_TOKEN"]

# 加载文件夹中的所有txt类型的文件
loader = PyPDFLoader('/Users/yuanrongjie/Downloads/S16技术方案.pdf')
# 将数据转成 document 对象，每个文件会作为一个 document
documents = loader.load()

# 初始化加载器
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
# 切割加载的 document
split_docs = text_splitter.split_documents(documents)

# 初始化 openai 的 embeddings 对象
# embeddings = OpenAIEmbeddings(openai_api_type="azure",openai_api_base = os.environ["AZURE_OPENAI_ENDPOINT"],openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],open_api_version = os.environ["OPENAI_API_VERSION"])
embeddings = AzureOpenAIEmbeddings(model="text-embedding-3-large")
# 将 document 通过 openai 的 embeddings 对象计算 embedding 向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
docsearch = Chroma.from_documents(split_docs, embeddings, persist_directory="/Users/yuanrongjie/software/python_project/crawerSet/temp_Chroma")

# 创建问答对象
qa = RetrievalQA.from_chain_type(
    llm=AzureOpenAI(
    deployment_name="gpt-4o"), 
    chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)
# 进行问答
result = qa({"query": "车辆信息在test环境测试的账号是什么？"})
print(result)