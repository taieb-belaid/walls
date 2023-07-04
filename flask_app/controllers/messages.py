from flask_app import app
from flask_app.models.message import Message
from flask import request,redirect

@app.route('/send_message',methods=['POST'])
def send_message():
    Message.save(request.form)
    return redirect('/walls') 

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id':id
    }
    Message.delete(data)
    return redirect('/walls')