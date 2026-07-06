from langchani_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parser import StrOutputParser

laod_dotenv()



prompt1 = PromptTemplate(
    prompt="Generate a detail report on topic {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Generate a 5 pointer summary from the following text \n {text}",
    input_variables=['text']
)
model = ChatOpenAI()
parser = StrOutputParser()
chain = prompt1 | model | parser | prompt2 | model | parser

chain.invoke({"topic" : "Unployement in India"})