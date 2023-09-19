from flask import Flask, send_from_directory, redirect, request, render_template
import openai
from pydantic import BaseModel

with open("../config.txt", "r") as f:
    api_key = f.read().strip()
    openai.api_key = api_key

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return redirect('/origin')

class HTMLAIResponse(BaseModel):
    code: str

def generate(userRequest):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a machine that generates websites with full HTML, CSS, and JavaScript in one file."},
            {"role": "user", "content": """You are a machine that generates a website based on the requests of a user.
                                            You will be given their request, and your job is to generate the full HTML
                                            file of a website that fits their request.  You can use CSS and JavaScript to
                                            make the website look good and add functionality if needed.  You can also use any HTML
                                            tags you want and use CSS to make the website's appearance match the theme of the request.
                                            Double check your code to make sure it works right and correct any mistakes. Finally, somewhere in
                                            you code, include a button that links to /origin .
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
    return output[12:-3]


global lastQuery
lastQuery = ""

@app.route('/origin', methods=['GET'])
def home():
    global lastQuery
    if request.method == 'GET' and "q" in request.args:
        if request.args["q"] == "": return redirect('/origin')
        elif request.args["q"] == lastQuery: 
            print("serving lastQuery")
            try:
                return send_from_directory(app.root_path, path='gen.html')
            except:
                return redirect('/origin')
        else: 
            print("generating")
            lastQuery = request.args["q"]
            html = generate(lastQuery)
            with open("gen.html", "w") as f:
                f.write(html)
                f.close()
            return send_from_directory(app.root_path, path='gen.html')
    return send_from_directory(app.static_folder, path='index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)