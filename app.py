import json

from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)


def get_allowed_groups():
    with open('./data/user.json', 'r') as file:
        numbers = json.load(file)
    return [str(num) for num in numbers]


@app.route('/')
def main():
    path = f'./files'
    elements = os.listdir(path)

    allowed_groups = get_allowed_groups()
    groups = [element for element in elements if not os.path.isfile(os.path.join(path, element)) and element in allowed_groups]

    return render_template("index.html", groups=groups)


@app.route('/view', methods=['GET', 'POST'])
def view_files():
    args = request.args

    path = f'./files/{args["group_id"]}'
    files = os.listdir(path)
    filenames = [f for f in files if os.path.isfile(os.path.join(path, f))]

    return render_template("view.html", files=filenames, group_id=args["group_id"], allowed=(args["group_id"] in get_allowed_groups()))


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
    return "Signup"


@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login"


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
