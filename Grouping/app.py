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
