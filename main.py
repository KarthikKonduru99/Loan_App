from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loan_app.db'
db = SQLAlchemy(app)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    term = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(20), default='PENDING')  # PENDING, APPROVED, PAID
    repayments = db.relationship('Repayment', backref='loan', lazy=True)

class Repayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='PENDING')  # PENDING, PAID
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)

def calculate_repayment_schedule(loan):
    start_date = datetime.now().date()
    repayment_amount = loan.amount / loan.term

    schedule = []
    for i in range(loan.term):
        due_date = start_date + timedelta(weeks=(i + 1))
        schedule.append({
            'due_date': due_date,
            'amount': repayment_amount,
            'status': 'PENDING'
        })

    return schedule

@app.route('/create_loan', methods=['POST'])
def create_loan():
    data = request.json

    new_loan = Loan(amount=data['amount'], term=data['term'])
    db.session.add(new_loan)
    db.session.commit()

    repayment_schedule = calculate_repayment_schedule(new_loan)
    for repayment in repayment_schedule:
        new_repayment = Repayment(
            amount=repayment['amount'],
            due_date=repayment['due_date'],
            loan=new_loan
        )
        db.session.add(new_repayment)

    db.session.commit()

    return jsonify({'message': 'Loan created successfully', 'loan_id': new_loan.id}), 201

@app.route('/approve_loan/<int:loan_id>', methods=['PATCH'])
def approve_loan(loan_id):
    loan = Loan.query.get(loan_id)

    if loan:
        loan.state = 'APPROVED'
        db.session.commit()
        return jsonify({'message': 'Loan approved successfully'}), 200
    else:
        return jsonify({'error': 'Loan not found'}), 404

@app.route('/view_loans/<int:customer_id>', methods=['GET'])
def view_loans(customer_id):
    loans = Loan.query.filter_by(id=customer_id).all()

    if loans:
        loan_data = []
        for loan in loans:
            loan_data.append({
                'id': loan.id,
                'amount': loan.amount,
                'term': loan.term,
                'state': loan.state,
                'repayments': [{'due_date': r.due_date, 'amount': r.amount, 'status': r.status} for r in loan.repayments]
            })

        return jsonify({'loans': loan_data}), 200
    else:
        return jsonify({'message': 'No loans found for the customer'}), 404

@app.route('/add_repayment/<int:loan_id>', methods=['POST'])
def add_repayment(loan_id):
    loan = Loan.query.get(loan_id)
    data = request.json

    if loan:
        repayments = loan.repayments
        for repayment in repayments:
            if repayment.status == 'PENDING' and repayment.due_date == datetime.strptime(data['due_date'], '%Y-%m-%d').date() and data['amount'] >= repayment.amount:
                repayment.status = 'PAID'
                db.session.commit()


        if all(repayment.status == 'PAID' for repayment in repayments):
            loan.state = 'PAID'
            db.session.commit()
        return jsonify({'message': 'Repayment added successfully'}), 200

        # return jsonify({'error': 'No pending repayments found for the given due date and amount'}), 404
    else:
        return jsonify({'error': 'Loan not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)