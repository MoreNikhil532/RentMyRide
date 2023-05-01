# RentMyRide

RentMyRide is a web application built with Django, which allows users to rent vehicles from a variety of available options.

## Installation

1. Clone the repository
   ```
   git clone https://github.com/username/RentMyRide.git
   ```
2. Create a virtual environment and activate it
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies
   ```
   pip install -r requirements.txt
   ```
4. Run the migrations
   ```
   python manage.py migrate
   ```
5. Create a superuser account
   ```
   python manage.py createsuperuser
   ```
6. Run the server
   ```
   python manage.py runserver
   ```
7. Open `http://localhost:8000` in your browser to view the application.

## Usage

1. Users can create an account to start renting vehicles.
2. The website displays available vehicles along with their details such as brand, model, and price per day.
3. Users can select a vehicle they want to rent and specify the rental period.

## License

This project is licensed under the [MIT License](LICENSE).
