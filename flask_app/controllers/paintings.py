from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.painting import Painting
from flask_app.models.user import User




# -----------------------------------------------------------------------------

@app.route('/new/painting')
def new_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new_painting.html',user=User.get_by_id(session['user_id']))

@app.route('/create/painting',methods=['POST'])
def create_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect('/new/painting')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": int(request.form["price"]),
        "quantity": int(request.form["quantity"]),
        "user_id": session["user_id"]
    }
    Painting.save(data)
    return redirect('/dashboard')

@app.route('/edit/painting/<int:id>')
def edit_painting(id):
    data = {
        "id":id
    }
    if 'user_id' not in session:
        return redirect('/logout')
    painting = Painting.get_one(data)
    if session['user_id'] != painting.user_id:
        return redirect('/logout')
    return render_template("edit_painting.html",edit=Painting.get_one(data),user=User.get_by_id(session['user_id']))

@app.route('/update/painting',methods=['POST'])
def update_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect(f'/edit/painting/{request.form["id"]}')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": int(request.form["price"]),
        "quantity": int(request.form["quantity"]),
        "id": request.form['id']
    }
    Painting.update(data)
    return redirect('/dashboard')

@app.route('/painting/<int:id>')
def show_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template("show_painting.html",painting=Painting.get_one(data),user=User.get_by_id(session['user_id']),owned=Painting.owned_painting())

@app.route('/destroy/painting/<int:id>')
def destroy_painting(id):
    data = {
        "id": id
    }
    if 'user_id' not in session:
        return redirect('/logout')
    painting = Painting.get_one(data)
    if session['user_id'] != painting.user_id:
        return redirect('/logout')
    Painting.destroy(data)
    return redirect('/dashboard')

@app.route('/buy/painting/<int:id>')
def buy_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id": session["user_id"],
        "id" : id
    }
    Painting.buy_painting(data)
    Painting.update_inventory(data)
    return redirect('/dashboard')