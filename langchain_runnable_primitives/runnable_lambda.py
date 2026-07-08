from langchain_openai import ChatOpenAI
from langchain_runnable import runnable_lambda, runnable_sequence, runnable_passthrough, runnable_parallel

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def word_count(text):
    return len(text.split())

model = ChatOpenAI()
parser = StrOutputParser()

prompt = PromptTemplate(
    template="write a joke about {topic}",
    input_variables=["topic"]
)

joke_gen_chain = runnable_sequence(prompt, model, parser)

parallel_chain = runnable_parallel({
    "joke" : runnable_passthrough(),
    "word_count" : runnable_lambda(word_count)

})

final_chain = runnable_sequence(joke_gen_chain, runnable_parallel)

result = final_chain.invoke({"topic" : "AI"})

final_result = """{} \n word count - {}""".format(result['joke'], result['word_count'])

print(final_result)
