import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

gemini_url='https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=GEMINI_API_KEY'
load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api)
def ai_review(url:str) -> dict:

    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt =f"""Url:{url}
        Go to product Url and Analyze this product info for a retail customer. Provide:
        1. A 50-word summary
        2. Three usage tips as bullet points
        3. Three key features as bullet points
        in json format
        
        Product Information:
        -[product info]
        
        Format your response as:
        Summary: [summary text]
        Usage Tips:
        - [tip 1]
        - [tip 2]
        - [tip 3]
        Features:
        - [feature 1]
        - [feature 2]
        - [feature 3]"""
    res = model.generate_content(prompt)
    #print(res.text[7:-3])
    result=json.loads(res.text[7:-3])
    return result

if __name__ =='__main__':
    ans=ai_review('https://www.walmart.com/ip/Shark-Cordless-Pet-Stick-Vacuum-for-Carpet-and-Hard-Floors-with-Anti-Allergen-Complete-Seal-IX140H/321730943?classType=VARIANT&athbdg=L1600')

