# Automatic Login and Class Schedule Management

This project is a Python application that allows university students to automatically log into their school system and manage their class schedules. The program uses an SQLite database to store user information and class schedules. Additionally, it utilizes Selenium WebDriver to automatically log in to the school system at the specified time.

## Features
- **User Registration and Login System:** Users can register with their name, school number, and password, and then log in to the system.
- **Class Schedule Management:** Users can add or update their class schedule by specifying the date, start time, and end time.
- **Automatic Login:** The program sets a random time within +/- 5 minutes of the class start time and automatically logs in to the system.
- **Schedule-Based Program Start:** The program automatically starts and logs in according to the user-defined schedule.
- **Quick Start for Testing:** A quick start mode is available to test the automatic login process.

## Usage
- Ensure that the required Python libraries (sqlite3, selenium, datetime, etc.) are installed before running the program.
- Use the `veritabani_olustur()` function to create the necessary tables.
- On the main screen, users can log in or register.
- After logging in, users can add or update their class schedule, start the program according to the schedule, or use the quick start mode.

## Requirements
- Python 3.x
- SQLite
- Selenium WebDriver
- Google Chrome and ChromeDriver

## Setup
1. Clone or download this repository.
2. Install the requirements:
   ```bash
   pip install selenium
   ```
3. Install Google Chrome and ChromeDriver.
4. Run the program using the following command:
   ```bash
   python program.py
   ```

## Notes
- The program uses Google Chrome installed on the user's computer. Ensure that ChromeDriver is in the correct path.
- This project aims to automate timely class attendance and also serves as a learning resource for Python and Selenium usage.

## Contributing
Contributions are welcome! Fork the repository and submit a pull request for any improvements or new features.
