import mysql.connector
from tkinter import *
from tkinter import messagebox

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",       # Replace with your MySQL username
    password="ABC@123abc",   # Replace with your MySQL password
    database="flight_db"
)
cursor = conn.cursor()

# GUI Setup
root = Tk()
root.title("Flight Booking System")

# Input Fields
Label(root, text="Passenger ID").grid(row=0, column=0, padx=10, pady=5, sticky=W)
passenger_entry = Entry(root)
passenger_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Seat Number").grid(row=1, column=0, padx=10, pady=5, sticky=W)
seat_entry = Entry(root)
seat_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Select Flight").grid(row=2, column=0, padx=10, pady=5, sticky=W)
flight_var = StringVar(root)
flight_var.set("101 - IndiGo")  # Default selection
flight_dropdown = OptionMenu(root, flight_var, "101 - IndiGo", "102 - Air India", "103 - SpiceJet")
flight_dropdown.grid(row=2, column=1, padx=10, pady=5)

# Booking Function
def book_flight():
    passenger_id = passenger_entry.get()
    seat_number = seat_entry.get()
    flight_id = flight_var.get().split(" ")[0]  # Extract flight ID

    # Check if passenger exists
    cursor.execute("SELECT * FROM Passenger WHERE passenger_id = %s", (passenger_id,))
    if not cursor.fetchone():
        messagebox.showerror("Error", "Passenger ID not found. Please register passenger first.")
        return

    # Check if seat is already booked
    cursor.execute("SELECT * FROM Booking WHERE flight_id = %s AND seat_number = %s", (flight_id, seat_number))
    if cursor.fetchone():
        messagebox.showerror("Error", "Seat already booked!")
        return

    # Insert booking
    try:
        cursor.execute(
            "INSERT INTO Booking (passenger_id, flight_id, seat_number) VALUES (%s, %s, %s)",
            (passenger_id, flight_id, seat_number)
        )
        conn.commit()
        messagebox.showinfo("Success", "Flight booked successfully!")

        # Show booking summary
        messagebox.showinfo("Booking Summary",
                            f"Passenger ID: {passenger_id}\nFlight: {flight_id}\nSeat: {seat_number}")

        # Clear fields
        passenger_entry.delete(0, END)
        seat_entry.delete(0, END)
        flight_var.set("101 - IndiGo")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))

# Dashboard Function
def show_dashboard():
    dashboard = Toplevel(root)
    dashboard.title("Booking Dashboard")

    Label(dashboard, text="All Bookings", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10)

    cursor.execute("SELECT * FROM Booking")
    rows = cursor.fetchall()

    for i, row in enumerate(rows, start=1):
        Label(dashboard, text=str(row)).grid(row=i, column=0, padx=10, pady=2, sticky=W)

# Buttons
Button(root, text="Book Flight", command=book_flight, bg="lightblue").grid(row=3, column=0, columnspan=2, pady=10)
Button(root, text="View Bookings", command=show_dashboard, bg="lightgreen").grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()