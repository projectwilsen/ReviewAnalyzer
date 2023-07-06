import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import textwrap
from transformers import pipeline

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["huggingfacehub_api_token"]

repo_id = "tiiuae/falcon-7b-instruct"  
falcon_llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_new_tokens": 400}
)

rm = 'deepset/roberta-base-squad2'

question_answerer = pipeline("question-answering", model=rm)

df = pd.read_csv('E:\\projectsupertype\\ReviewAnalyzer\\rHux0gMZ3Eg_comment.csv')

# pos = df[df['sentiment'] == 'positive']
# neg = df[df['sentiment'] == 'negative']

def summary_of_comments(df,things = 'positive'):
    filtered_comment = df[df['sentiment'] == things]
    comment_text = ';'.join(filtered_comment['comment_text']).replace('\n','')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
    comment_doc = text_splitter.create_documents([comment_text])

    output = {}
    for i in comment_doc:
        result = question_answerer(question= f"What {things} things does the user/audience feel?", context= i.page_content) #str(i)
        output[result['answer']] = round(result['score'], 4)
        print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")
        
    keys_set = set(output.keys())
    keys_sentence = '; '.join([key for key in keys_set])
    print(keys_sentence)

    docs = text_splitter.create_documents([keys_sentence])
    print('done splitting')

    chain = load_summarize_chain(falcon_llm, chain_type="map_reduce", verbose=True)
    print(chain.llm_chain.prompt.template)
    print(chain.combine_document_chain.llm_chain.prompt.template)

    output_summary = chain.run(docs)
    wrapped_text = textwrap.fill(
        output_summary, width=100, break_long_words=False, replace_whitespace=False
    )
    print(wrapped_text)

    return wrapped_text


negative_comment = summary_of_comments(df,'negative')
print(negative_comment)

positive_comment = summary_of_comments(df,'positive')
print(positive_comment)

# # pos_comment = ';'.join(pos['comment_text']).replace('\n','')
# neg_comment = ';'.join(neg['comment_text']).replace('\n','')

# print(neg_comment)

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
# neg_comment_doc = text_splitter.create_documents([neg_comment])



# output = {}
# for i in neg_comment_doc:
#     result = question_answerer(question= "What bad things does the user/audience feel?", context= i.page_content) #str(i)
#     output[result['answer']] = round(result['score'], 4)
#     print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")
    
# keys_set = set(output.keys())
# keys_sentence = '; '.join([key for key in keys_set])
# print(keys_sentence)

# docs = text_splitter.create_documents([keys_sentence])
# print('done splitting')

# chain = load_summarize_chain(falcon_llm, chain_type="map_reduce", verbose=True)
# print(chain.llm_chain.prompt.template)
# print(chain.combine_document_chain.llm_chain.prompt.template)

# output_summary = chain.run(docs)
# wrapped_text = textwrap.fill(
#     output_summary, width=100, break_long_words=False, replace_whitespace=False
# )
# print(wrapped_text)