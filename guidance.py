import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import YoutubeLoader
import textwrap

df = pd.read_csv('E:\\projectsupertype\\Youtube\\rHux0gMZ3Eg_comment.csv')

positive_comments = df[df['sentiment'] == 'positive']

# Convert the filtered data to a string
positive_comments_str = ';'.join(positive_comments['comment_text']).replace('\n','')

# Print the result
print(positive_comments_str)

#comments = '; '.join(df['comment_text']).replace('\n','')

# print("done load comments")

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["huggingfacehub_api_token"]

repo_id = "tiiuae/falcon-7b-instruct"  
falcon_llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.1, "max_new_tokens": 500}
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
docs = text_splitter.create_documents([positive_comments_str])
print('done splitting')

chain = load_summarize_chain(falcon_llm, chain_type="map_reduce", verbose=True)
print(chain.llm_chain.prompt.template)
print(chain.combine_document_chain.llm_chain.prompt.template)

output_summary = chain.run(docs)
wrapped_text = textwrap.fill(
    output_summary, width=100, break_long_words=False, replace_whitespace=False
)
print(wrapped_text)

# # postemplate = """

# # Based on {input}, you should find positive things/product/service being liked by the audience/consument. 

# #   """

# # posprompt = PromptTemplate(input_variables=["input"],template=postemplate)
# # poschain = LLMChain(llm=falcon_llm, prompt=posprompt)
# # result = []
# # for i in docs:
# #     output = poschain.run(input = i.page_content)
# #     result.append(output)
# #     print(output)
# #     print("done")

# # print(result)
