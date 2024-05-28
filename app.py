import json

from flask import Flask, request, render_template, send_from_directory, session, redirect, flash
import os

import crypto_utils
import data_handler
import utils

app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_allowed_groups():
    return ["1", "2", "3"]


def read_write_json(new_data, filename='data/users.json'):
    with open(filename, 'r') as file:
        data = json.load(file)

    # Step 2: Append the new account details to the account_details list
    data['account_details'].append(new_data)

    # Step 3: Write the updated JSON data back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def load_users():
    with open('data/users.json', 'r') as file:
        return json.load(file)['account_details']


def verify_password(stored_password, salt, provided_password):
    return stored_password == crypto_utils.hash_password(provided_password, bytes.fromhex(salt)).hex()


@app.route('/')
def main():
    if not session.get('user'):
        return redirect("/login")
    path = f'./files'
    elements = os.listdir(path)

    allowed_groups = get_allowed_groups()
    groups = [element for element in elements if
              not os.path.isfile(os.path.join(path, element)) and element in allowed_groups]

    return render_template("index.html", groups=groups)


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        args = request.args

        file = request.files['file']

        name = file.filename
        if '/' in name:
            name = file.filename[name.rfind('/') + 1:]

        file_path = f'./files/{args['group_id']}/{name}'

        # If the file exists, add the count to the name: e.g. "cat (1).jpg"
        if os.path.isfile(file_path):
            base, extension = os.path.splitext(file.filename)
            counter = 1
            new_file_path = f'./files/{args['group_id']}/{base} ({counter}){extension}'
            while os.path.isfile(new_file_path):
                counter += 1
                new_file_path = f'./files/{args['group_id']}/{base} ({counter}){extension}'
            file_path = new_file_path

        file.save(file_path)
        return render_template("upload.html")


@app.route('/download', methods=['GET'])
def download_file():
    if request.method == 'GET':
        args = request.args
        return send_from_directory(f'./files/{args['group_id']}', args['filename'], as_attachment=True)


# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get("user"):
        return render_template("signup.html")
    else:
        return redirect("/")


@app.route('/post_signup', methods=['GET'])
def post_signup():
    if request.method == 'GET':
        args = request.args
        email = args['email']
        password = args['password']
        salt = crypto_utils.generate_salt()
        hashed_password = crypto_utils.hash_password(password, salt)
        userid = utils.generate_uuid()

        if not utils.validate_input(password, 8):
            error = "Password must be 8 characters long"
            return render_template("error.html", error=error), {"Refresh": "2; url=/signup"}

        account_details = {
            'userid': userid,
            'email': email,
            'salt': salt.hex(),
            'hashed_password': hashed_password.hex()
        }

        read_write_json(account_details)

        return f'Email: {email} - Password: {password}'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get("user"):
        return render_template("login.html")
    else:
        return redirect("/")


@app.route('/post_login', methods=['GET'])
def post_login():
    args = request.args
    email = args['email']
    password = args['password']

    users = load_users()
    for user in users:
        if user['email'] == email:
            if verify_password(user['hashed_password'], user['salt'], password):
                session['user'] = email
                return redirect("/")
            else:
                return f'wrong but: {email},{password}'
    return 'Invalid Credentials'


@app.route('/user/<user_id>', methods=['GET', 'POST'])
def view_groups(user_id):

    group_ids = data_handler.get_group_ids(user_id)

    return render_template('user.html', user_id=user_id, groups=group_ids)


@app.route('/user/<user_id>/group/<group_id>', methods=['GET'])
def view_files(user_id, group_id):

    files = data_handler.get_files(group_id)
    permissions = data_handler.get_permissions(user_id, group_id)

    if permissions:
        return render_template('group.html', group_id=group_id, files=files, allow_add=permissions['allow_add'], allow_delete=permissions['allow_delete'])
    else:
        return redirect("/")


# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==


if __name__ == '__main__':
    app.run()
