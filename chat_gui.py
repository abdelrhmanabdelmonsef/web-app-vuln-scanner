import random
import time

import mesop as me
import mesop.labs as mel
from try1 import exploitation1 

@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/chat",
  title="Mesop Demo Chat",
)
def page():
  mel.chat(transform, title="web app Vuln-Scanner", bot_user="your hacker")

  

  
def transform(input: str, history: list[mel.ChatMessage]):
    r=f(input)
    return r
  

def f(input):
   return input*10




   