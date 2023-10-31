from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Replace with your desired SQLite database file path
db = SQLAlchemy(app)


class Data(db.Model):
    CustomerNo = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Text)
    NameAddress = db.Column(db.Text)
    FFNameAddress = db.Column(db.Text)
    Similarity = db.Column(db.Integer)
    Status = db.Column(db.Text)
    UnderReview = db.Column(db.Text)
    Timestamp = db.Column(db.DateTime)
    UserAudit = db.Column(db.Text)
    Comment = db.Column(db.Text)

app.app_context().push()
db.create_all()


# Function to populate the database from CSV files
def populate_database():
    import csv
    import os

    csv_files = [
        '../BGMaxFiles/2023/Jan/Matched/BM000020-BGMAX- - 20230102_output.csv',
        '../BGMaxFiles/2023/Feb/Matched/BM000041 BGMAX- - 01 20230201_output.csv'
    ]

    for csv_file in csv_files:
        if os.path.exists(csv_file):
            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data = Data(
                        CustomerNo=int(row['CustomerNo']),
                        Date=row['Date'],
                        NameAddress=row['NameAddress'],
                        FFNameAddress=row['FFNameAddress'],
                        Similarity=int(row['Similarity']),
                        Status='',
                        UnderReview='',
                        Timestamp='',
                        UserAudit='',
                        Comment=''
                    )
                    db.session.add(data)
    db.session.commit()


# Call the populate_database function to initially populate the database
populate_database()

@app.route('/', methods=['GET', 'POST'])
def display_data():
    if request.method == 'POST':
        current_customer_no = int(request.form['current_customer_no'])
        next_customer_no = current_customer_no + 1
    else:
        current_customer_no = db.session.query(Data).order_by(Data.CustomerNo).first().CustomerNo
        next_customer_no = current_customer_no + 1

    data = Data.query.filter_by(CustomerNo=current_customer_no).all()

    return render_template('index.html', data=data, next_customer_no=next_customer_no)

@app.route('/next', methods=['POST'])
def next_group():
    current_customer_no = int(request.form['current_customer_no'])
    next_customer_no = current_customer_no + 1

    return redirect(url_for('display_data', next_customer_no=next_customer_no))

if __name__ == '__main__':
    app.run(debug=True)
