import json

from flask import Flask, request, render_template, send_from_directory, session, redirect
import os

import crypto_utils
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


@app.route('/view', methods=['GET', 'POST'])
def view_files():
    args = request.args

    path = f'./files/{args["group_id"]}'
    files = os.listdir(path)
    filenames = [f for f in files if os.path.isfile(os.path.join(path, f))]

    return render_template("view.html", files=filenames, group_id=args["group_id"],
                           allowed=(args["group_id"] in get_allowed_groups()))


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


@app.route('/account/<user_id>', methods=['GET'])
def account(user_id):
    return f'User: {user_id}'


@app.route('/group/<group_id>', methods=['GET'])
def group(group_id):
    return f'Group: {group_id}'


@app.route('/group/<group_id>/folder/<folder_id>', methods=['GET'])
def folder(group_id, folder_id):
    return f'Group: {group_id} - Folder: {folder_id}'


# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==


if __name__ == '__main__':
    app.run()
