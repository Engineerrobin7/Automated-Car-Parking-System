import random
import string
import sqlite3
from tkinter import *
from tkinter import messagebox
from twilio.rest import Client
import qrcode
from PIL import Image, ImageTk

# Twilio credentials (Replace these with your Twilio credentials)
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_phone_number = 'your_twilio_phone_number'

# Database setup
def create_db():
    with sqlite3.connect('parking_system.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS parked_vehicles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        vehicle_number TEXT,
                        vehicle_name TEXT,
                        owner_name TEXT,
                        mobile_number TEXT,
                        slot TEXT,
                        token TEXT,
                        payment_status TEXT)''')
        conn.commit()

# Generate random token
def generate_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Send token via SMS using Twilio
def send_sms(mobile_number, token):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your parking token is: {token}",
            from_=twilio_phone_number,
            to=mobile_number
        )
        print(f"Token sent to {mobile_number}")
    except Exception as e:
        print(f"Error sending SMS: {e}")
        messagebox.showerror("Error", "Failed to send SMS. Please check your credentials.")

# Fetch available slots (Mocked for simplicity)
def fetch_available_slots():
    slots = ['Slot 1', 'Slot 2', 'Slot 3', 'Slot 4']
    return slots

# Park the vehicle
def park_vehicle():
    vehicle_number = vehicle_number_entry.get()
    vehicle_name = vehicle_name_entry.get()
    owner_name = owner_name_entry.get()
    mobile_number = mobile_number_entry.get()
    slot = slot_var.get()

    if not vehicle_number or not vehicle_name or not owner_name or not mobile_number or slot == "No Slots Available":
        messagebox.showerror("Error", "Please fill all fields correctly!")
        return

    token = generate_token()
    send_sms(mobile_number, token)

    with sqlite3.connect('parking_system.db') as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO parked_vehicles (vehicle_number, vehicle_name, owner_name, mobile_number, slot, token, payment_status)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''', (vehicle_number, vehicle_name, owner_name, mobile_number, slot, token, 'Not Paid'))
        conn.commit()

    messagebox.showinfo("Vehicle Parked", f"Vehicle parked in {slot}. Token: {token}")
    update_parked_list()

# Update the parked vehicles list
def update_parked_list():
    with sqlite3.connect('parking_system.db') as conn:
        c = conn.cursor()
        c.execute('SELECT vehicle_number, vehicle_name, owner_name, slot, token, payment_status FROM parked_vehicles')
        vehicles = c.fetchall()

    parked_list.delete(0, END)
    for vehicle in vehicles:
        parked_list.insert(END, f"{vehicle[0]} - {vehicle[1]} ({vehicle[2]}) | Slot: {vehicle[3]} | Token: {vehicle[4]} | Payment: {vehicle[5]}")

# Mark payment as Paid (Cash)
def pay_fees():
    slot = payment_slot_entry.get()
    if not slot:
        messagebox.showerror("Error", "Please enter a slot number.")
        return

    with sqlite3.connect('parking_system.db') as conn:
        c = conn.cursor()
        c.execute('''UPDATE parked_vehicles SET payment_status = 'Paid' WHERE slot = ? AND payment_status = 'Not Paid' ''', (slot,))
        conn.commit()

    messagebox.showinfo("Payment Status", f"Payment for Slot {slot} marked as paid (Cash).")
    update_parked_list()

# Generate QR code for payment
def generate_qr_code(slot):
    if not slot:
        messagebox.showerror("Error", "Please enter a slot number.")
        return

    payment_link = f"https://example.com/pay?slot={slot}"
    qr = qrcode.make(payment_link)
    qr.show()

# Remove vehicle from parking
def remove_vehicle():
    slot = remove_slot_entry.get()
    token = remove_token_entry.get()

    if not slot and not token:
        messagebox.showerror("Error", "Please enter either a Slot Number or a Token to remove the vehicle.")
        return

    with sqlite3.connect('parking_system.db') as conn:
        c = conn.cursor()
        # Use the token or slot to identify the vehicle to remove
        if slot:
            c.execute("DELETE FROM parked_vehicles WHERE slot = ?", (slot,))
            conn.commit()
            messagebox.showinfo("Vehicle Removed", f"Vehicle in Slot {slot} has been removed successfully.")
        elif token:
            c.execute("DELETE FROM parked_vehicles WHERE token = ?", (token,))
            conn.commit()
            messagebox.showinfo("Vehicle Removed", f"Vehicle with Token {token} has been removed successfully.")

    # Update parked vehicles list after removal
    update_parked_list()

# Create GUI
def create_gui():
    global vehicle_number_entry, vehicle_name_entry, owner_name_entry, mobile_number_entry, slot_var, parked_list, payment_slot_entry, remove_slot_entry, remove_token_entry

    root = Tk()
    root.title("Automated Car Parking System")
    root.geometry("600x750")

    # Title
    title_label = Label(root, text="Automated Car Parking System", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # Parking Section
    park_frame = Frame(root)
    park_frame.pack(pady=10)

    vehicle_number_label = Label(park_frame, text="Vehicle Number:")
    vehicle_number_label.grid(row=0, column=0, padx=5, pady=5)
    vehicle_number_entry = Entry(park_frame, width=20)
    vehicle_number_entry.grid(row=0, column=1, padx=5, pady=5)

    vehicle_name_label = Label(park_frame, text="Vehicle Name:")
    vehicle_name_label.grid(row=1, column=0, padx=5, pady=5)
    vehicle_name_entry = Entry(park_frame, width=20)
    vehicle_name_entry.grid(row=1, column=1, padx=5, pady=5)

    owner_name_label = Label(park_frame, text="Owner Name:")
    owner_name_label.grid(row=2, column=0, padx=5, pady=5)
    owner_name_entry = Entry(park_frame, width=20)
    owner_name_entry.grid(row=2, column=1, padx=5, pady=5)

    mobile_number_label = Label(park_frame, text="Mobile Number:")
    mobile_number_label.grid(row=3, column=0, padx=5, pady=5)
    mobile_number_entry = Entry(park_frame, width=20)
    mobile_number_entry.grid(row=3, column=1, padx=5, pady=5)

    slot_label = Label(park_frame, text="Choose Slot:")
    slot_label.grid(row=4, column=0, padx=5, pady=5)
    slot_var = StringVar(root)
    available_slots = fetch_available_slots()
    slot_var.set(available_slots[0] if available_slots else "No Slots Available")
    slot_menu = OptionMenu(park_frame, slot_var, *available_slots)
    slot_menu.grid(row=4, column=1, padx=5, pady=5)

    park_button = Button(park_frame, text="Park Vehicle", command=park_vehicle)
    park_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Payment Section
    payment_frame = Frame(root)
    payment_frame.pack(pady=10)

    payment_slot_label = Label(payment_frame, text="Slot Number for Payment:")
    payment_slot_label.grid(row=0, column=0, padx=5, pady=5)
    payment_slot_entry = Entry(payment_frame, width=20)
    payment_slot_entry.grid(row=0, column=1, padx=5, pady=5)

    qr_button = Button(payment_frame, text="Generate QR Code", command=lambda: generate_qr_code(payment_slot_entry.get()))
    qr_button.grid(row=1, column=0, padx=5, pady=5)

    cash_button = Button(payment_frame, text="Mark as Paid (Cash)", command=pay_fees)
    cash_button.grid(row=1, column=1, padx=5, pady=5)

    # Remove Vehicle Section
    remove_frame = Frame(root)
    remove_frame.pack(pady=10)

    remove_label = Label(remove_frame, text="Remove Vehicle", font=("Arial", 14, "bold"))
    remove_label.grid(row=0, column=0, columnspan=2, pady=5)

    remove_slot_label = Label(remove_frame, text="Slot Number:")
    remove_slot_label.grid(row=1, column=0, padx=5, pady=5)
    remove_slot_entry = Entry(remove_frame, width=20)
    remove_slot_entry.grid(row=1, column=1, padx=5, pady=5)

    remove_token_label = Label(remove_frame, text="Token:")
    remove_token_label.grid(row=2, column=0, padx=5, pady=5)
    remove_token_entry = Entry(remove_frame, width=20)
    remove_token_entry.grid(row=2, column=1, padx=5, pady=5)

    remove_button = Button(remove_frame, text="Remove Vehicle", command=remove_vehicle)
    remove_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Parked Vehicles List
    parked_frame = Frame(root)
    parked_frame.pack(pady=10)

    parked_label = Label(parked_frame, text="Parked Vehicles", font=("Arial", 14, "bold"))
    parked_label.grid(row=0, column=0, columnspan=2, pady=5)

    parked_list = Listbox(parked_frame, width=60, height=10)
    parked_list.grid(row=1, column=0, columnspan=2)

    # Initialize DB and fetch parked vehicles
    create_db()
    update_parked_list()

    root.mainloop()

create_gui()
