from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parser import StrOutputParser
from dotenv import load_dotenv

from langchain.schema.runnable import RunnableSequence

load_dotenv()

prompt = PromptTemplate(
    template="write a joke about {topic}",
    input_variables=["topic"]
)

model = ChatOpenAI()
parser = StrOutputParser()

prompt2 = PromptTemplate(
    template="Explain the following joke - {text}",
    input_varibales=['text']
)

# chain = prompt | model | parser

chain = RunnableSequence(prompt, model, parser, prompt2, model, parser)

result = chain.invoke({"topic": "cricket"})
print(result)