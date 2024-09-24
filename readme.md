# Candidate Search Functionality using Django ORM

This project implements a search functionality for a candidate database. It returns candidates based on the relevancy of the search query, giving priority to exact matches followed by partial matches, which are sorted by the number of overlapping words with the query.

## Features

- **Exact Match**: Candidates whose names exactly match the query appear first.
- **Partial Match**: Candidates whose names partially match the query appear after exact matches.
- **Relevancy Sorting**: Partial matches are sorted based on the number of overlapping words with the query.

## Project Setup

### Prerequisites

- Python 3.x
- Django 3.x or higher

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd <repo-url>

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv env
   source env/bin/activate

3. Install dependencies:

   ```bash
   pip install -r requirements.txt

4. Apply migrations:
   ```bash
   python manage.py migrate


5. Running Tests
   You can run the test suite using Django's built-in test runner:

   python manage.py test