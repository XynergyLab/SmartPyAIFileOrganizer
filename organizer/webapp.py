# webapp.py
from flask import Flask, render_template_string
import sqlite3
from config import DATABASE_NAME

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, file_path, file_name, file_extension, file_size, created_time, modified_time FROM files")
    files = cursor.fetchall()
    conn.close()
    template = """
    <!doctype html>
    <html>
      <head>
        <title>File Metadata</title>
      </head>
      <body>
        <h1>Scanned File Metadata</h1>
        <table border="1">
          <tr>
            <th>ID</th>
            <th>File Path</th>
            <th>File Name</th>
            <th>Extension</th>
            <th>Size</th>
            <th>Created</th>
            <th>Modified</th>
          </tr>
          {% for file in files %}
          <tr>
            <td>{{ file[0] }}</td>
            <td>{{ file[1] }}</td>
            <td>{{ file[2] }}</td>
            <td>{{ file[3] }}</td>
            <td>{{ file[4] }}</td>
            <td>{{ file[5] }}</td>
            <td>{{ file[6] }}</td>
          </tr>
          {% endfor %}
        </table>
      </body>
    </html>
    """
    return render_template_string(template, files=files)

if __name__ == "__main__":
    app.run(debug=True)
