from flask import Flask,render_template,redirect,url_for,request
import uuid

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

tasks = [{"id":"f217cfe5-98e5-4164-afe6-80d9c54bab11", "title":"task1", "status":"completed", "description":"test1 task is done"}]

@app.get("/")
@app.get("/home")
def home():
    return render_template("home.html", tasks=tasks)

@app.get('/form/<reson>/<task_id>')
def task_form(reson, task_id):
    try:
        status = ""
        action = ""
        task = []
        if reson == "create":
            status = "create"
            action = "/create"
        elif reson == "edit": 
            status = "edit"
            action = f"/edit/{task_id}"
            task = [task for task in tasks if task["id"] == task_id]
        else:
            status = "show"
            action = f"/show/{task_id}"
            task = [task for task in tasks if task["id"] == task_id]
            
        return render_template('task.html', form_status=status, action=action, task=task[0] if task else None)
    except Exception:
        return "Error show task form",500

@app.post("/create")
def create_task():
    try:
        print(request.form.get("title"))
        tasks.append({"id":str(uuid.uuid4()),
                    "title":request.form.get("title"), 
                    "status":request.form.get("status1"),
                    "description":request.form.get("description")})
        return redirect(url_for("home"))
    except Exception:
        return "Error creating task",500
    
@app.post("/edit/<task_id>")
def edit_task(task_id):
    try:
        for task in tasks:
            if task["id"] == task_id:
                task["title"] = request.form.get("title")
                task["status"] = request.form.get("status1")
                task["description"] = request.form.get("description")
                
        return redirect(url_for("home"))
    except Exception:   
        return "Error editing task", 500

@app.post("/delete_task/<task_id>")
def delete_task(task_id):
    try:
        global tasks
        tasks = [task for task in tasks if task["id"] != task_id]
            
        return redirect(url_for("home"))
    except Exception:   
        return "Error deleting task", 500

@app.post("/import_excel")
def import_excel():
    try:
        import pandas as pd
        import os
        global tasks
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'static', 'data.xlsx')
        xls = pd.ExcelFile(file_path)
        existing_ids = {task['id'] for task in tasks}
        
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            dict_list = df.to_dict('records')
            for item in dict_list:
                task_id = str(item.get('id')).strip()
                if task_id in existing_ids:
                    continue
                task_dict={
                    'id': item.get('id'),
                    'title': item.get('title'),
                    'status': item.get('status'),
                    'description': item.get('description')
                }
                tasks.append(task_dict)
                existing_ids.add(task_id)
        return redirect(url_for("home"))
    except Exception:   
        return "Error importing excel", 500
        
@app.get("/download_tasks")
def download_tasks():   
    try:
        import json
        global tasks
        with open('data_task.json', 'w') as file:
            file.write(json.dumps(tasks, indent=4)) 
        return redirect(url_for("home"))
    
    except Exception :   
        return "Error downloading tasks", 500
    
    
if __name__ == "__main__":
    app.run() 