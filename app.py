#import flask
from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy #for data base
from datetime import datetime
#setup applictation
app = Flask(__name__)#reference this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'#Telling our app where our data base is located ////=> absolute path ///=> relative path
#Data Base initialisation
db = SQLAlchemy(app)#our data base is intialised with the settings for app
#create Model
class Todo(db.Model):#Todo Model
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime , default =datetime.utcnow)
    #Every time we create a new element it returns task id that been created
    def __rep__(self):
        return '<Task %r>' % self.id
#create index route #Decorator ### so that when we browse the url we dont emmidiatlly fall in 404 and flask set up route with th app route decorator 
@app.route('/', methods=['POST','GET'])#url string of url ?? #Option method adding 2 methods so we can get and post by default we have only Get
#define the function for the route
def index():
    if request.method == 'POST':#if request send to this route is post
        #Create a new task from the input
        task_content = request.form['content']#request object form that wweve createted and we pass the id of the input that we want to get the content of#task content = content of the input in the form
        #Todo object
        new_task = Todo(content=task_content)#content of that input

        try:
            db.session.add(new_task)#we add to our data base session
            db.session.commit()#commit to our data base
            return redirect('/')#redirect back to our index page
        except:
            return 'issue'
        


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()#look at all the data base contents and the order that they ve been created and return all of them#first => the most recent
        return render_template('index.html',tasks=tasks)#render_template so it return the html file#tasks variable that we created
#Setup a new route for delete
@app.route('/delete/<int:id>')#id name of the virable
def delete(id):
    #task that we want to delete
    task_to_delete = Todo.query.get_or_404(id)#attempt to get that task by the id and if it doesn't exist its gonna just 404

    try:
        db.session.delete(task_to_delete)#(the task that we want to delete)
        db.session.commit()#commit?
        return redirect('/')#to the home page
    except:
        return 'there was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])#because we are gonna be posting
def update(id):
    task = Todo.query.get_or_404(id)#Were getting the task from the id and were passing it to the url
    if request.method == 'POST':
        task.content = request.form['content']#setting the current  task content to the ceontent in the form!!?
        try:
            db.session.commit()#we just need to commit because we are not adding we are just updating
            return redirect('/')#sending us to the home page
        except:#eception
            return 'Issue updating the task'
    else:
        return render_template('update.html',task=task) 


if __name__ == "__main__":
    app.run(debug=True)#so if we have errors it will pop up in web page and we can see
