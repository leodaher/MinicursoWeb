from flask import Flask, jsonify 
import mongoengine as me

class User(me.Document):
	name = me.StringField()
	email = me.StringField()

class ToDo(me.Document):
	description = me.StringField()
	deadline = me.DateTimeField()
	title = me.StringField()
	finished = me.BooleanField()
	tags = me.ListField(me.StringField())
	added = me.DateTimeField()
	user = me.ReferenceField(User)
	color = me.StringField()

app = Flask(__name__)
me.connect("todo_app")

@app.route("/users", methods=['GET'])
def get_users():
	users = User.objects.all()
	array = []
	for user in users:
		array.append({
			'id': str(user.id),
			'name': user.name,
			'email': user.email
		})

	return jsonify(array)

if __name__ == "__main__":
	app.run()