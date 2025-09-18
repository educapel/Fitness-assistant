#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import minsearch


# In[61]:


df = pd.read_csv('data.csv')
#df.drop('id', axis=1, inplace=True)


# In[25]:


get_ipython().system('wget https://raw.githubusercontent.com/alexeygrigorev/minsearch/main/minsearch.py')


# In[27]:


df.columns


# In[62]:


documents = df.to_dict(orient='records')
documents


# ## Ingestion

# In[63]:


index= minsearch.Index(
    text_fields = [ 'exercise_name', 'type_of_activity', 'type_of_equipment',
       'body_part', 'type', 'muscle_groups_activated', 'instructions'],
    keyword_fields=['id']
)



# In[64]:


query = 'give me leg exercises for hamstring'


# In[65]:


index.fit(documents)


# In[35]:


index.search(query, num_results=10)


# In[47]:


import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key found: {api_key is not None}")


# ## Rag flow

# In[49]:


from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

response = client.chat.completions.create(
  extra_body={},
  model="deepseek/deepseek-chat-v3.1:free",
  messages=[
    {
      "role": "user",
      "content": query
    }
  ]
)
print(response.choices[0].message.content)


# In[50]:


def search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[52]:


documents[0]


# In[66]:


prompt_template = """
You're a figness instuctor. Answer the QUESTION based on the CONTEXT from our exercises database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

entry_template = """
exercise_name: {exercise_name}
type_of_activity: {type_of_activity}
type_of_equipment: {type_of_equipment}
body_part ; {body_part}
type : {type}
muscle_groups_activated : {muscle_groups_activated}
instructions : {instructions}
""".strip()

def build_prompt(query, search_results):

    context = ""

    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


# In[67]:


search_results = search(query)
prompt = build_prompt(query, search_results)


# In[59]:


def llm(prompt):
    response = client.chat.completions.create(
    extra_body={},
    model="deepseek/deepseek-chat-v3.1:free",
     messages=[
        {
          "role": "user",
          "content": query
        }
      ]
    )

    return response.choices[0].message.content


# In[57]:


def rag(query):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer


# In[68]:


answer = rag(query)
print(answer)


# In[ ]:




