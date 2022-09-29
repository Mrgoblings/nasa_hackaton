from flask import Flask, render_template
import json

app = Flask(__name__, template_folder="./htmls", static_folder='staticFiles')


def take_question(number):
    with open('staticFiles/questions.json', encoding="utf8") as file:
        text = json.loads(file.read())
        question = 'q' + str(number)
        return text['quiz'][question]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quiz")
def quiz():
    question = take_question(1)
    return render_template("quiz.html", question=question["question"],
                           answer_0=question["options"][0], answer_1=question["options"][1],
                           answer_2=question["options"][2], answer_3=question["options"][3])


@app.route("/info")
def info():
    return render_template("info.html")


app.run(port=5000, debug=True)
