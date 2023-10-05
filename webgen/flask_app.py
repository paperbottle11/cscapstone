from flask import Flask, send_from_directory, redirect, request
from generate import generate

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return redirect('/origin')

global lastQuery
lastQuery = ""

@app.route('/origin', methods=['GET'])
def home():
    global lastQuery
    if request.method == 'GET' and "q" in request.args:
        if request.args["q"] == "": return redirect('/origin')
        elif request.args["q"] == lastQuery: 
            # Returns the last generated site if the query is the same as the last one
            print("serving lastQuery")
            try:
                return send_from_directory("gen", "gen.html")
            except:
                return redirect('/origin')
        else: 
            # Generates a new website if the query is different from the last one
            print("generating")
            html, css, js = generate(request.args["q"])

            # Inserts a home button into the generated site with its styling
            insertIdx = html.find("<body>")
            html = html[:insertIdx+6] + "\n<a id=\"home\" href=\"/origin\">Home</a>\n" + html[insertIdx+6:]
            css = "#home {\ndisplay: block;\npadding: 10px 20px;\ntext-decoration: none;\nborder-radius: 5px;\nborder-style: solid;\nborder-width: 1px;\nfont-weight: bold;\nbackground-color: #ddd;\ncolor: black;\nfloat: left;\n}\n#home:hover {\nbackground-color: #555;\ncolor: white;\n}\n" + css
            
            # Writes the generated site to the gen folder
            with open("gen/gen.html", "wb") as f:
                f.write(html.encode())
                f.close()
            with open("gen/gen.css", "wb") as f:
                f.write(css.encode())
                f.close()
            with open("gen/gen.js", "wb") as f:
                f.write(js.encode())
                f.close()
            
            # Save the current query as the last query
            lastQuery = request.args["q"]
            print("serving generated site")
            return send_from_directory("gen", "gen.html")
    return send_from_directory(app.static_folder, path="index.html")

# Serves gen files from the gen folder
@app.route('/gen/<path:filename>')
def gen_assets(filename):
    return send_from_directory("gen", filename)

# Serves the last generated site
@app.route('/lastgen')
def lastgen():
    try:
        return send_from_directory("gen", "gen.html")
    except:
        return redirect('/origin')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)