from flask import Flask, render_template, request
import json

app = Flask(__name__, template_folder="./htmls", static_folder='staticFiles')

BAD_REQUEST = "400 - Bad reqeust"

# clients = []


def take_question(number):
    with open('staticFiles/questions.json', encoding="utf8") as file:
        text = json.loads(file.read())
        question = 'q' + str(number)
        return text['quiz'][question]


def check_question_query(query):
    # return {"question", "last_chosen_answer", "points"}.issubset(set(query.keys())
    return (not all(key in query for key in ["question", "last_chosen_answer", "points"]) and
            int(query["question"]) > 0 and int(query["points"]) > 0)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quiz", methods=["GET"])
def quiz():
    query = request.args.to_dict()
    print(query)
    question = {}

    if not query:
        question = take_question(1)
        # create_new_client()
    else:
        if check_question_query(dict(query)):
            print("1")
            return BAD_REQUEST

        prev_question = take_question(int(query["question"]) - 1)
        question = take_question(int(query["question"]))

        if query["last_chosen_answer"] not in prev_question["options"]:
            print("2")
            print(f"q [{query['last_chosen_answer']}] -- last - .[{prev_question['options']}].")
            return BAD_REQUEST

    try:
        return render_template("quiz.html", question=question["question"],
                               answer_0=question["options"][0], answer_1=question["options"][1],
                               answer_2=question["options"][2], answer_3=question["options"][3])
    except:
        return BAD_REQUEST


@app.route("/info")
def info():
    return render_template("info.html")


# @app.route("/iamalive",  methods=["GET"])
# def iamalive():
#     token = request.args.to_dict()["token"]
#     for client in clients:
#         if client["token"] == token:
#             client["last_seen"] = datetime.datetime.now()
#

app.run(port=5000, debug=True)


# 127.0.0.1:5000/quiz?question=3&last_chosen_answer=Консенсусът+е,+че+е+едновременно+реалено+и+създадено+от+човека.&points=4