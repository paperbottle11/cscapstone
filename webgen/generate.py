import openai
import json
from pydantic import BaseModel

class WebsiteAIResponse(BaseModel):
    html: str
    css: str
    js: str

def generate(userRequest):
    with open("../config.txt", "r") as f:
        api_key = f.read().strip()
        openai.api_key = api_key
        f.close()
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a machine that generates a website with HTML, CSS, and JavaScript."},
            {"role": "user", "content": "You will be given a request, generate HTML, CSS, and JavaScript code for a website that fits the request.  Use any HTML tags you need, and use CSS to make the website look good. Make sure the code works and correct any mistakes.  In the HTML code, the href of the stylesheet is \"/gen/gen.css\" and the src of the javascript file is \"/gen/gen.js\".  Create the full java script needed for the request. If the request is a game, make the full javascript for the game.   Create the full CSS code needed to make it look good.  The request is: " + userRequest}
        ],
        functions=[
            {
            "name": "create_website",
            "description": "Create a website based on the given request",
            "parameters": WebsiteAIResponse.model_json_schema()
            }
        ],
        function_call={"name": "create_website"}
    )
    output = json.loads(response.choices[0]["message"]["function_call"]["arguments"])
    return output["html"], output["css"], output["js"]