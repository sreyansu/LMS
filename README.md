# Library Management System

A Flask-based web application for managing a library's books, members, and book lending operations.

## Features

- **Book Management**
  - Add, edit, and delete books
  - Track book availability and quantity
  - Search and filter books by various criteria

- **Member Management**
  - Add, edit, and delete library members
  - Track member details and membership status
  - Different member types (student, faculty)

- **Issue/Return Management**
  - Issue books to members
  - Track due dates and returns
  - Calculate and manage fines for late returns
  - View issue history

- **Dashboard**
  - Overview of total books, members, and issued books
  - Quick access to all major functions
  - Real-time statistics

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd CRUD
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
```bash
python3 app.py
```

3. Open your web browser and navigate to:
```
http://127.0.0.1:5001
```

## Database

The application uses SQLite as its database. The database file (`library.db`) will be automatically created when you first run the application. The system comes pre-populated with:

- 10 default books
- 4 default members
- 5 sample issue records

## Project Structure

```
CRUD/
├── app.py              # Main application file
├── library.db          # SQLite database
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS, images)
│   └── css/
│       └── styles.css
└── templates/         # HTML templates
    ├── about.html
    ├── books.html
    ├── index.html
    ├── issue.html
    └── members.html
```

## Features in Detail

### Book Management
- Add new books with details like title, author, ISBN, publisher, etc.
- Edit existing book information
- Delete books from the system
- Track book availability and quantity

### Member Management
- Register new members with personal details
- Update member information
- Delete member records
- Different member types (student/faculty)

### Issue/Return System
- Issue books to members
- Set due dates for returns
- Process book returns
- Calculate and manage fines for late returns
- Track issue history

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 