import csv
from flask import Flask, render_template

app = Flask(__name__)

# Read data from CSV file
def read_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

@app.route('/')
def index():
    # Read data from CSV and pass it to the template
    data = read_csv('BM000020-BGMAX- - 20230102_output.csv')
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
