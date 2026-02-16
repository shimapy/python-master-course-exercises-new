from flask import Flask,render_template,redirect,url_for,request
import uuid

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

personal_info = [{"id":"f217cfe5-98e5-4164-afe6-80d9c54bab11", "first_name":"shima", "last_name":"monzavi", 
                  "age":"25", "interesting":"Painting", "score":"10" ,"description":"i love painting"}]
SCORE_VALUES = [1,2,3,4,5,6,7,8,9,10]
INTEREST_VALUES = ['Painting', 'Programming', 'Sports', 'Calligraphy']

@app.get("/")
@app.get("/home")
def home():
    return render_template("home.html", persons=personal_info)

@app.route("/create", methods=['GET', "POST"])
def create_person():
    try:
        if request.method == 'GET':
            return render_template("form.html", Interestings=INTEREST_VALUES, scores=SCORE_VALUES)
        else:
            personal_info.append({"id":str(uuid.uuid4()),
                                "first_name":request.form.get("first_name"), 
                                "last_name":request.form.get("last_name"),
                                "age":request.form.get("age"),
                                "interesting":request.form.get("Interesting1"),
                                "score":request.form.get("score"),
                                "description":request.form.get("description")})
            # return redirect(url_for("form"))
            return render_template("form.html", Interestings=INTEREST_VALUES, scores=SCORE_VALUES)
    except Exception as e:
        print(str(e))
        return "Error creating task",500
    
if __name__ == "__main__":
    app.run() 