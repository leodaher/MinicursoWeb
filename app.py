from flask import Flask, jsonify, request 
import mongoengine as me
import datetime

class User(me.Document):
	name = me.StringField()
	email = me.StringField()

	def to_dict(self):
		return {
			'id': str(self.id),
			'name': self.name,
			'email': self.email
		}

class Task(me.Document):
	description = me.StringField()
	deadline = me.DateTimeField()
	title = me.StringField()
	finished = me.BooleanField()
	tags = me.ListField(me.StringField())
	added = me.DateTimeField()
	user = me.ReferenceField(User)
	color = me.StringField()

	def to_dict(self):
		return {
			'id': str(self.id),
			'title': self.title,
			'description': self.description,
			'finished': self.finished,
			'tags': self.tags,
			'added': int(self.added.timestamp()),
			'user': str(self.user.id),
			'color': self.color,
			'deadline': int(self.deadline.timestamp())
		}

app = Flask(__name__)
me.connect("todo_app")

@app.route("/users", methods=['GET'])
def get_users():
	users = User.objects.all()
	array = []
	for user in users:
		array.append(user.to_dict())

	return jsonify(array)

@app.route("/users", methods=['POST'])
def create_user():
	if not request.is_json:
		return jsonify({'error':'not_json'}), 400
	data = request.get_json()
	name = data.get('name')
	email = data.get('email')
	user = User(name=name, email=email)
	user.save()
	return jsonify(user.to_dict())

@app.route("/tasks", methods=['GET'])
def get_tasks():
	tasks = Task.objects.all()
	array = []
	for task in tasks:
		array.append(task.to_dict())

	return jsonify(array)

@app.route("/tasks", methods=['POST'])
def create_task():
	if not request.is_json:
		return jsonify({'error':'not_json'}), 400
	data = request.get_json()
	task = Task(finished=False, added=datetime.datetime.now())
	task.title = data.get('title')
	task.description = data.get('description')
	task.tags = data.get('tags', [])
	task.deadline = datetime.datetime.fromtimestamp(data.get('deadline', 0))
	task.color = data.get('color')
	task.user = User.objects.filter(id=data.get('user')).first()
	task.save()
	
	return jsonify(task.to_dict())

@app.route("/tasks/<string:task_id>", methods=['PATCH'])
def update_tasks(task_id):
	if not request.is_json:
		return jsonify({'error':'not_json'}), 400
	task = Task.objects.filter(id=task_id)
	if not task:
		return jsonify({'error':'not_found'}), 404
	data = request.get_json()
	task.finished = data.get('finished', task.finished)
	task.save()
	return jsonify(task.to_dict())

if __name__ == "__main__":
	app.run()