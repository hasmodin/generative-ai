from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.output-parser import StrOutputParser
from langchain_prompts import PromptTemplate
from langchain_schema.runnable import RunnableParallel, RunnableBranch, RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic impor BaseModel, Field

load_dotenv()


model = ChatOpenAI()

parser = StrOutputParser()

class Feedback(BaseModel) :
    sentiment : Literal["positive", "negative"] = Field(description="Give the sentiment of the feedback")

parser2 = PydanticOutputParser(pydantic_object=Feedback)  


prompt1 = PromptTemplate(
    template="Classify the sentiment fo the following feedback text into postive or negative \n {feedback} \n {formate_instructions}",
    input_variables=["feedback"]
    partial_variables={"format_instruction:" : parser2.get_format_instructions}
)

classifier_chain = prompt1 | model | parser2

# result = classifier_chain.invoke({"feedback" : "This is a terrible smartphone"}).sentimate
# print(result)

prompt2 = PromptTemplate(
    template="Write an appropriate reponse to this positive feedback \n {feedback}",
    input_varibales=["feedback"]
)

prompt3 = PromptTemplate(
    template="Write an appropriate reponse to this negative feedback \n {feedback}",
    input_varibales=["feedback"]
)

branch_chain = RunnableBranch(
    (lambda x:x.sentiment == "positive", prompt2 | model1 | parser),
    (lambda x:x.sentiment == "negative", prompt3 | model1 | parser),
    RunnableLambda(lambda x: "could not find sentiment")
)

final_chain = classifier_chain | branch_chain

result = final_chain.invoke({"feedback": "This is a terrible phone"})