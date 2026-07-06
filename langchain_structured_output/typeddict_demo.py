from typing import TypedDict

class Person(TypedDict):

    name : str
    age : int


new_person: Person = {"name": "Ehan", "age" : 7}

print(new_person)

import streamlit as st
