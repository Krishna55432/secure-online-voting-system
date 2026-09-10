# Secure Online Voting System

A secure web-based online voting system developed using Python and Flask. The system provides voter authentication, OTP verification, electoral roll validation, duplicate-vote prevention, blockchain-based vote recording, and election result management.

## Features

- Voter login and authentication
- OTP-based verification
- Electoral roll validation
- One-person-one-vote mechanism
- Duplicate voting prevention
- Blockchain-based vote recording
- Tamper-evident vote storage
- Admin dashboard
- Election result display
- Invalid login and OTP handling
- Candidate information and images
- Vote status tracking

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Blockchain
- CSV

## Project Structure

secure-online-voting-system/
│
├── app.py
├── blockchain.py
├── database.py
├── chain.json
├── electoral_roll_1000.csv
│
├── static/
│   ├── aiadmk.png
│   ├── annamalai.png
│   ├── bjp.png
│   ├── dmk.png
│   ├── eps.png
│   ├── stalin.png
│   ├── tvk.png
│   └── vijay.png
│
├── templates/
│   ├── admin.html
│   ├── already.html
│   ├── chain.html
│   ├── invalid_login.html
│   ├── invalid_otp.html
│   ├── login.html
│   ├── otp.html
│   ├── result.html
│   ├── success.html
│   └── vote.html
│
├── .gitignore
└── README.md

## How the System Works

1. The voter enters their login credentials.
2. The system validates the voter using the electoral roll.
3. An OTP verification process is performed.
4. After successful verification, the voter can access the voting page.
5. The voter selects a candidate and submits the vote.
6. The vote is recorded using the blockchain component.
7. The system checks and prevents duplicate voting.
8. The administrator can view the blockchain and election results.

## Blockchain-Based Vote Recording

The system uses a blockchain component to maintain a tamper-evident record of votes.

Each block is linked with the previous block using cryptographic hashing. This helps maintain the integrity of voting records and makes unauthorized modifications easier to detect.

## Security Features

- Voter authentication
- OTP verification
- Electoral roll validation
- Duplicate-vote prevention
- Blockchain-based vote integrity
- Administrator functionality
- SQLite database storage

## Installation

### 1. Clone the Repository

git clone https://github.com/Krishna55432/secure-online-voting-system.git

cd secure-online-voting-system

### 2. Install Dependencies

pip install flask

### 3. Run the Application

python app.py

### 4. Open in Browser

http://127.0.0.1:5000

## Database

The project uses SQLite for storing application data.

The database file is generated locally and is excluded from the Git repository using .gitignore.

## Future Enhancements

- Production-grade authentication
- Real SMS/Email OTP integration
- Role-based access control
- Digital signatures
- Advanced audit logging
- Secure cloud deployment
- Improved blockchain consensus mechanism
- Multilingual support
- Accessibility improvements

## Disclaimer

This project is developed for educational and academic purposes. It is a prototype and should not be used for real public elections without additional security auditing, testing, legal compliance, and production-grade infrastructure.

## Author

Krishna Manokaran

GitHub: https://github.com/Krishna55432
