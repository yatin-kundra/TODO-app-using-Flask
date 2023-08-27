from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 


app = Flask(__name__)   # refrencing to the current file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"        # telling our app wehre our database if located and name of of our database if test.db
db = SQLAlchemy(app)

# creating a model 
class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)



    def __repr__(self):
        return '<Task %r' % self.id     # evertime we creat a task till will return that task and id of that task


@app.route("/", methods = ['POST', 'GET'])     # "/" tells that this is the home page of the app
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = TODO(content = task_content)

        # pushing to the database 
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        # creating an exception 
        except:
            return 'there was an issue adding yout list.'

    else:
        task = TODO.query.order_by(TODO.date_created).all()  # just sorting all the tasks by date
        return render_template('index.html', task = task)


# to delete a task from the list.
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TODO.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "There was a problem deleting that task"


# to update the task from the list.
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):

    task = TODO.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'There was some problem updating your task'
    else:
        return render_template('update.html', task = task)

if __name__ == "__main__":
    app.run(debug=True)         # debug is true so that if there are anyerrors then they will pop on the page



    # terminal commands: 
    # (0)   python          // run the following commnads in python terminal
    # (1)   from app import app, db
    # (2)   app.app_context().push()
    # (3)   db.create_all()

    #  these commands are for creating a database and it will be created under instance folder 