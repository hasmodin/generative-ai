from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from regex import template

from langchain_runnable import runnable_passthrough, runnable_sequence, runnable_parallel

load_dotenv()

prompt = PromptTemplate(
    template="write a joke about {topic}",
    input_variables=["topic"]
)

model = ChatOpenAI()
parser = StrOutputParser()

prompt2 = PromptTemplate(
    template="Explain the following joke - {text}",
    input_variables=['text']
)

joke_gen_chain = runnable_sequence(prompt, model, parser)

parallel_chain = runnable_parallel({
    "joke" : runnable_passthrough(),
    "explanation" : runnable_sequence(prompt2, model, parser)
})

final_chain = runnable_sequence(joke_gen_chain, parallel_chain)

print(final_chain.invoke({"topic" : "cricket"}))