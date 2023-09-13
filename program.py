import openai
from pydantic import BaseModel

with open("config.txt", "r") as f:
    api_key = f.read()
    openai.api_key = api_key

class HTMLAIResponse(BaseModel):
    code: str

userRequest = input("What do you want to make: ")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "system", "content": "You are a machine that generates websites with full HTML, CSS, and JavaScript in one file."},
        {"role": "user", "content": """You are a machine that generates a website based on the requests of a user.
                                         You will be given their request, and your job is to generate the full HTML
                                         file of a website that fits tzheir request.  You can use CSS and JavaScript to
                                         make the website look good and add functionality if needed.  You can also use any HTML
                                         tags you want and use CSS to make the website's appearance match the theme of the request.
                                         Double check your code to make sure it works right and correct any mistakes.
                                         Their request is: """ + userRequest}
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
print(output)

with open("output.html", "w") as f:
    f.write(output[11:-2])
    f.close()