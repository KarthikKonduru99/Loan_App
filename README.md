# Loan Application
## Overview
This is a web application that allows authenticated users to go through a loan application process. Users can submit a loan request specifying the amount and term, and after approval, they can submit weekly repayments.

## Features
### Loan Creation:

Customers can submit a loan request specifying the amount and term.
Example: Requesting $10,000 with a term of 3 weeks starting from 7th Feb 2022.
Generates 3 scheduled repayments with amounts and dates.

### Admin Approval:

Admins can change the state of PENDING loans to APPROVED.

### Loan Viewing:
Customers can view their own loans.
Policy check ensures customers can view only their own loans.
### Repayment:
Customers can add repayments with amounts greater or equal to the scheduled repayment.
Scheduled repayment status changes to PAID upon successful repayment.
If all scheduled repayments for a loan are PAID, the loan becomes PAID automatically.


## Getting Started

To get started with the project, follow these steps:

1. Clone the repository.
2. Set up a virtual environment.
3. Install the project dependencies by running `pip install -r requirements.txt` within the virtual environment.
4. Configure the database settings in the project's file
5. Run the development server using the command `python main.py`.
6. You will the flask application running on 'http://127.0.0.1:5000'
