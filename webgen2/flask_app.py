from flask import Flask, send_from_directory, redirect, request
from pathlib import Path
from base64 import b64decode
import cv2
import numpy as np
import openai
import json
from pydantic import BaseModel

def byte_image_to_numpy(byte_image):
    np_array = np.frombuffer(byte_image, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return img

def show(img, wait=0):
    if type(img) is bytes:
        img = byte_image_to_numpy(img)
    cv2.imshow("img", img)
    cv2.waitKey(wait)

with open("../config.txt", "r") as f:
    api_key = f.read().strip()
    openai.api_key = api_key
    f.close()

def generateImage(prompt, debug=False):
    if debug:
        print("Debug mode is on, skipping image generation")
        return open("test.png", "rb").read()
    
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256",
        response_format="b64_json",
    )

    image_data = b64decode(response["data"][0]["b64_json"])
    return image_data

class WebsiteAIResponse(BaseModel):
    html: str
    image_names: list
    image_prompts: list

def generate(userRequest):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a machine that generates a website with HTML."},
            {"role": "user", "content": f"The request is: {userRequest}. Generate the HTML code with all of the content that would be in the request. Be informative. The href of the stylesheet is \"/generated/genstyle.css\". Create a list with the names of each image file that is used. Create a corresponding list with detailed captions for each image name. Position these images in the website using img tags with where they logically make sense. The folder where the images are located is called \"images\". The output must be valid json text."}
        ],
        functions=[
            {
            "name": "create_website",
            "description": "Create a website based on the given request and create image prompts for the images in the website",
            "parameters": WebsiteAIResponse.model_json_schema()
            }
        ],
        function_call={"name": "create_website"}
    )
    with open("json.json", "w") as f:
        f.write(response.choices[0]["message"]["function_call"]["arguments"])
        f.close()
    output = json.loads(response.choices[0]["message"]["function_call"]["arguments"].encode())
    return output["html"], output["image_names"], output["image_prompts"]

data_dir = Path.cwd() / "static" / "images"
data_dir.mkdir(exist_ok=True)
data_dir = Path.cwd() / "static" / "generated"
data_dir.mkdir(exist_ok=True)

app = Flask(__name__, static_folder="static")

@app.route('/', methods=['GET'])
def index():
    return redirect('/home')

global lastQuery
lastQuery = ""

@app.route('/home', methods=['GET'])
def home():
    global lastQuery
    if request.method == 'GET' and "q" in request.args:
        if request.args["q"] == "": return redirect('/home')
        elif request.args["q"] == lastQuery: 
            # Returns the last generated site if the query is the same as the last one
            print("serving lastQuery")
            try:
                return send_from_directory(app.static_folder, "generated/gen.html")
            except:
                return redirect('/home')
        else: 
            # Generates a new website if the query is different from the last one
            print("generating")
            html, image_names, image_prompts = generate(request.args["q"])
            
            # Inserts a home button into the generated site with its styling
            insertIdx = html.find("<body>")
            html = html[:insertIdx+6] + "\n<a id=\"home\" href=\"/home\">Home</a>\n" + html[insertIdx+6:]
            
            # Writes the generated site to the generated folder
            with open("static/generated/gen.html", "wb") as f:
                f.write(html.encode())
                f.close()
            
            print(image_names)
            print(image_prompts)
            # Generates images for each image prompt
            for name, prompt in zip(image_names, image_prompts):
                img = generateImage(prompt, debug=True)
                with open(f"static/images/{name}", "wb") as f:
                    f.write(img)
                    f.close()
            
            # Save the current query as the last query
            lastQuery = request.args["q"]
            print("serving generated site")
            return send_from_directory(app.static_folder, "generated/gen.html")
    return send_from_directory(app.static_folder, path="index.html")

@app.route('/generated/<path:filename>')
def web_gen_assets(filename):
    return send_from_directory("static/generated", filename)

@app.route('/images/<path:filename>')
def img_gen_assets(filename):
    return send_from_directory("static/images", filename)

@app.route('/lastgen')
def lastgen():
    try:
        return send_from_directory(app.static_folder, "generated/gen.html")
    except:
        return redirect('/home')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)