from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_runnable import runnable_branch, runnable_passthrough, runnable_lambda, runnable_sequence, runnable_parallel

from langchain_core.prompts import PromptTemplate

load_dotenv()

prompt1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Summarize the following text \n {text}",
    input_variables = ["text"]
)
model = ChatOpenAI()
parser = StrOutputParser()


report_gen_chain = runnable_sequence(prompt1, model, parser)

branch_chain = runnable_branch(
    (lambda x: len(x.split() > 500), runnable_sequence(prompt2, model, parser)),
    runnable_passthrough()

)

final_chain = runnable_sequence(report_gen_chain, branch_chain)

result = final_chain.invoke({"topic": "Russia vs Ukraine"})
print(result)
