import openai
from pydantic import BaseModel

class HTMLAIResponse(BaseModel):
    code: str

def generate(userRequest):
    with open("../config.txt", "r") as f:
        api_key = f.read().strip()
        openai.api_key = api_key
        f.close()
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a machine that generates websites with full HTML, CSS, and JavaScript in one file."},
            {"role": "user", "content": "You will be given a user's request, and your job is to generate the full HTML file of a website that fits their request.  Use CSS and JavaScript to make the website look good and add functionality if needed.  Use any HTML tags you need and use CSS to make the website's appearance match the theme of the request. Make sure your code works and correct any mistakes. Finally, somewhere in your code, include a button that links to /origin . Their request is: " + userRequest}
        ],
        functions=[
            {
            "name": "create_website",
            "description": "Create a website based on the user's request",
            "parameters": HTMLAIResponse.model_json_schema()
            }
        ],
        function_call={"name": "create_website"}
    )

    output = response.choices[0]["message"]["function_call"]["arguments"]
    return output[12:-3]