from flask import Flask,render_template

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")


@app.get("/")
@app.get("/home")
def home():
    return render_template("home.html", title="My Portfolio", home=False, skill=False, project=False)

@app.get("/Skills")
def skils_page():
    skill_list = [{"title":"Backend Development","items":["Python","Flask","C#","ASP.NET","RESTful API Design","JWT Authentication","ORM & Database Modeling"]},
                  {"title":"Databases","items":["SQL Server","MySQL","SQLite","Redis (Caching & Session Management)"]},
                  {"title":"Software Engineering","items":["OOP & Design Patterns","SOLID Principles","Clean Code","Basic System Design"]},
                  {"title":"Frontend Development","items":["HTML & CSS","Bootstrap","React.Js"]},
                  {"title":"Tools","items":["Git & GitHub","Postman & Soap ui","Bitbucket & Jira & Confluence","RedGate (SQL Compare & SQL DataCompare)"]}
                  ]
    return render_template("skill.html", title="Skills | My Portfolio",
                           skills=skill_list, home=True, skill=False, project=True)

@app.get("/Projects")
def project_page():
    project_list = [{"title":"Task Management System", 
                    "description":"A backend-focused task management system built with Flask.Includes user authentication, JWT, and CRUD operations.",          
                    "tech":"Flask · SQLite · JWT",
                    "github": "https://github.com/shimapy/python-master-course-exercises-new/tree/main/chapter3/Task_List_Project"},
                    {"title":"Portfolio Website Backend",
                    "description":"A simple backend application to serve a personal portfolio, demonstrating routing, templates, and clean project structure.",
                    "tech":"Flask · Jinja2",
                    "github": "https://github.com/shimapy/python-master-course-exercises-new/tree/main/chapter3/portfolio_Project"},
                    {"title":"Authentication API",
                    "description":"RESTful authentication API with token-based authentication, password hashing, and protected routes.",
                    "tech":"Flask · JWT · REST API",
                    "github": ""}
                    ]
    return render_template("project.html", title="Projects | My Portfolio",
                           projects=project_list, home=True, skill=True, project=False)


if __name__ == "__main__":
    app.run(debug= True)