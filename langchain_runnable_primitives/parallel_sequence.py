from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parser import StrOutputParser
from lanchain_chore.prompts import PromptTempalte
from lanchain.schema.runnable import RunnableSequence, RunnableParallel

load_dotenv()


model = ChatOpenAI()
parser = StrOutputParser()

prompt1 = PromptTemplate(
    template="Generate a tweet about {topic}",
    input_variables = ['topic']
)

prompt2 = PromptTemplate(
    template = "Generate a Linkedin post about {topic}",
    input_varibales = ['topic']
)


parallel_chain = RunnableParallel({
    "tweet" : RunnableSequence(prompt1, model, parser),
    "linkedin" : RunnableSequence(prompt2, model, parser)
})

print(parallel_chain.invoke({"topic": "AI"}))