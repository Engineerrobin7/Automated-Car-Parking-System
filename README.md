Automated Car Parking System
This is a Python-based Automated Car Parking System that provides an easy-to-use interface for parking vehicles, tracking parking slots, and generating tokens for each parked vehicle. The system also integrates Twilio for sending tokens via SMS to the user's mobile phone, and a payment system that supports both QR code generation for online payments and cash payments.

Features
Park New Vehicle: Users can park their vehicles and receive a unique token.
Payment System: Allows users to mark their parking fees as paid via cash or by scanning a QR code for online payment.
Token Generation: Each user receives a unique parking token sent to their mobile via SMS.
SQLite Database: The system uses SQLite to manage vehicle parking data.
Parking Slots Management: Displays available slots and assigns vehicles to them.
GUI: A user-friendly graphical interface built with Tkinter.
Technologies Used
Python 3: The primary programming language for developing the system.
Tkinter: A Python library used for creating the graphical user interface.
SQLite: A lightweight SQL database to store parked vehicle details.
Twilio API: Used to send SMS messages containing parking tokens.
QR Code Generation: For generating payment QR codes.
Setup and Installation
Prerequisites
Before running the system, you need to install the following libraries:

Twilio (for SMS functionality)
SQLite3 (for database functionality)
qrcode (for generating QR codes)
You can install the required Python packages using pip:

pip install twilio qrcode
Twilio Setup
Sign up on Twilio.
Get your Account SID, Auth Token, and Twilio Phone Number.
Replace account_sid, auth_token, and twilio_phone_number in the code with your own credentials.
Running the Application
Clone the repository to your local machine:

git clone https://github.com/yourusername/Automated-Car-Parking-System.git
cd Automated-Car-Parking-System
Run the Python script:

python parking_system.py
This will launch the GUI, allowing you to park vehicles, mark payments, and generate QR codes.

Features and How It Works
1. Park New Vehicle
The user can enter vehicle details like:
Vehicle Number
Vehicle Name
Owner Name
Mobile Number
Choose Parking Slot
After entering the details and clicking "Park Vehicle", the system will generate a unique token for the user and send it to their mobile number via SMS.
2. Generate QR Code
A QR code can be generated for payment using the "Generate QR Code" button. The user can scan it to complete their payment.
3. Mark as Paid
The user can mark the payment as paid (Cash) by entering the parking slot number and clicking "Mark as Paid (Cash)".
4. View Parked Vehicles
The system displays a list of currently parked vehicles, showing vehicle number, owner name, slot, token, and payment status.
File Structure
Automated-Car-Parking-System/
│
├── parking_system.py      # Main Python code for the parking system
├── parking_system.db      # SQLite database for storing vehicle and parking data
├── README.md              # Project description
├── requirements.txt       # List of required Python packages
Example Database Schema
The SQLite database has the following table structure:

CREATE TABLE IF NOT EXISTS parked_vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_number TEXT,
    vehicle_name TEXT,
    owner_name TEXT,
    mobile_number TEXT,
    slot TEXT,
    token TEXT,
    payment_status TEXT
);
Dependencies
Twilio: Used to send SMS messages with parking tokens.
SQLite3: To manage parking data.
Tkinter: To create the graphical user interface.
qrcode: To generate QR codes for online payment.
Future Enhancements
Integrate real-time parking slot availability updates.
Implement online payment via third-party gateways.
Add a notification system for vehicle expiration times.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Twilio for their SMS API.
Tkinter for GUI development.
qrcode for generating QR codes.
Make sure to replace placeholders (like yourusername) and credentials with your own information before using this README.md for your GitHub repository
