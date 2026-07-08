from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.output-parser import StrOutputParser
from langchain_prompts import PromptTemplate
from langchain_schema.runnable import RunnableParallel
load_dotenv()

model1 = ChatOpenAI()
model2 = ChatAnthropic(model_name="claud-3")

prompt1 = PromptTemplate(
    template="Generate short and simple notes from the following text \n {text}",
    input_variables=["text"]
)

prompt2 = PromptTemplate(
    template="Generate 5 short question answer from the following text \n {text}",
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template="Merge the provided notes and quiz into a single document \n notes -> {notes} and quiz -> {quiz}",
    input_varibales = ["notes", "quiz"]
)


parser = StrOutputParser()

parallel_chain = RunnableParallel({
    "notes" : prompt1 | model1 | parser,
    "quiz" : prompt2 | model2 | parser
})

merge_chain = prompt3 | model1 | parser

chain = parallel_chain | merge_chain

text = "Sheikh Tamim was commissioned as a second lieutenant in the Qatar Armed Forces upon graduation from Sandhurst.[1] He became the heir apparent to the Qatari throne on 5 August 2003, when his elder brother Sheikh Jassim renounced his claim to the title.[3][1] Since then he was groomed to take over rule, working in top security and economics posts.[2] On 5 August 2003, he was appointed deputy commander-in-chief of Qatar's armed forces.[1]

Sheikh Tamim promoted sport as part of Qatar's bid to raise its international profile.[2] In 2005 he founded Oryx Qatar Sports Investments, which owns Paris Saint-Germain F.C. among other investments. In 2006, he chaired the organizing committee of the 15th Asian Games in Doha. Under his leadership, all member countries attended the event for the first time in its history. That year's Al Ahram voted Tamim "the best sport personality in the Arab world".[1] Under his guidance, Qatar won the rights to host the 2014 FINA Swimming World Championships and the 2022 FIFA World Cup. Tamim is chairman of the National Olympic Committee.[1][2][4] At the 113th session of the International Olympic Committee (IOC) in February 2002, he was elected as a member of the IOC.[5] He headed Doha's bid for the 2020 Olympics.[1] The country hosted the 2022 FIFA World Cup. Qatar is estimated to have spent around $200 billion on infrastructure in preparation for the event.[6]

The Olympic Council of Asia (OCA) Evaluation Committee completed its tour to Doha in November 2020, and confirmed that the city will have much to offer for the Asian Games, and that they were satisfied with the prioritizing and support from Tamim.[7][8] At the 39th General Assembly of the OCA, President Ahmed Al-Fahad Al-Ahmed Al-Sabah announced that Doha would host the 2030 Asian Games.[9]

Sheikh Tamim heads the Qatar Investment Authority board of directors. Under his leadership, the fund has invested billions in British businesses. It owns large stakes in Barclays Bank, Sainsbury's, and Harrods.[10] The fund also owns a 95% share[11] of Europe's fourth tallest building, the Shard, a skyscraper in London.[2][12]

Tamim has also held a number of other posts, including:

Head of the Upper Council of the Environment and Natural Sanctuaries.[13]
Chairman of the Supreme Council for the Environment and Natural Reserves.[1]
Chairman of the Supreme Education Council.[1]
Chairman of the Supreme Council of Information and Communication Technology.[3]
Chairman of the board of directors of Public Works Authority (Ashghal) and the Urban Planning and Development Authority (UPDA).[3]
Chairman of the board of regents of Qatar University.[3]
Deputy chairman of the Ruling Family Council.[3]
Vice president of the Supreme Council for Economic Affairs and Investment.[3]
Deputy chairman of the High Committee for Coordination and Follow Up.[3]
Member of 'Sports for All'.[14]"



result = chain.invoke({"text" : "text"})

print(result)