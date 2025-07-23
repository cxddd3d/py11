# pip install langchain_openai


from langchain_openai.chat_models.base import BaseChatOpenAI

llm = BaseChatOpenAI(
    model='deepseek-chat', 
    openai_api_key='sk-fe3daef72fd14aaab31437e1dbd25f71',
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024
)

response = llm.invoke("如何学习AI")
print(response.content)