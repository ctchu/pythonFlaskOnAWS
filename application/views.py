# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 21:12:42 2015

@author: Randy
"""

from flask import render_template
from flask import request, redirect
from flask import jsonify
from flask import make_response
from flask import abort
from flask import url_for
from flask.ext.cors import cross_origin
#import logging
#logging.basicConfig(filename='.\\log\\logfile.log', filemode='w', level=logging.INFO)

from application import application

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

#===========================================
#===========================================
@application.route('/')
@application.route('/index')
def index_page():
    author = "Me"
    name = "Randy"
    return render_template('index.html', author=author, name=name)
    
#===========================================
#===========================================
@application.route('/signup', methods = ['POST'])
def sign_up():
    email = request.form['email']
    print("The email address is '" + email + "'")
    return redirect('/')
    
#===========================================
#===========================================    
@application.errorhandler(404) 
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#===========================================
#===========================================    
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task
    
#===========================================
#===========================================    
@application.route('/api/v1.0/tasks', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_tasks():
    #logging.info("test /api/v1.0/tasks api");
    #return jsonify({'tasks': tasks})   
    return jsonify({'tasks': map(make_public_task, tasks)})
    
#===========================================
#===========================================
@application.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

#===========================================
#===========================================    
@application.route('/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': 5,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
## Correct curl cmd in windows: curl -i -H "Content-Type: application/json" -X POST -d {"""title""":"""Read a book"""} http://localhost:5000/api/v1.0/tasks

#===========================================
#===========================================
@application.route('/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})
### Correct curl command in windowsL : curl -i -H "Content-Type: application/json" -X PUT -d {"""done""":true} http://localhost:5000/api/v1.0/tasks/2
    
#===========================================
#===========================================
@application.route('/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})