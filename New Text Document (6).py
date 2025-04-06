import csv
import os
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

with open("doctors.csv", mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)

root = tk.Tk()
root.title("Doctor's Presence System")
root.geometry("700x400")

style = ttk.Style()
style.theme_create("dark_azure", parent="alt", settings={
    "TButton": {
        "configure": {"background": "#166e80", "foreground": "#FFFFFF"},
        "map": {
            "background": [("active", "#005BBB"), ("disabled", "#2E3A44")],
            "foreground": [("disabled", "#D3D3D3")]
        }
    },
    "TLabel": {
        "configure": {"background": "#1C1C1C", "foreground": "#007FFF"}
    },
    "TFrame": {
        "configure": {"background": "#1C1C1C"}
    },
    "TEntry": {
        "configure": {"fieldbackground": "#007FFF", "foreground": "#FFFFFF"}
    }
})
style.theme_use("dark_azure")

frame = ttk.Frame(root, padding="10")
frame.pack(fill="both", expand=True)

label = ttk.Label(frame, text="کنگره پزشکی ایران", font=("Arial", 30))
label.pack(pady=20)
result_label = ttk.Label(frame, text="")
result_label.pack(pady=10)
result_label.place(x=30, y=120, width=200, height=20)
scanned_barcodes = set()
entry = ttk.Entry(frame)
entry.pack(pady=20)
entry.place(x=30, y=90, width=200, height=20)
file_label_entry = ttk.Entry(frame)
file_label_entry.pack(pady=20)
file_label_entry.place(x=30, y=350, width=150, height=20)
file_label_entry.insert(0, "attendance.csv")

def restart_app():
    root.destroy()
    os.system('python "New Text Document (6).py"')

def create_csv_file(event=None):
    filename = file_label_entry.get()
    current_date = datetime.now().strftime("%Y-%m-%d")
    directory = f'{current_date}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f'{directory}/{filename}', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Barcode", "FirstName", "LastName", "MedicalDegree", "Status"])
    result_label.config(text=f"CSV file {filename} created in {directory}")

def show_file_label_entry():
    file_label_entry.pack(pady=20)
    file_label_entry.place(x=30, y=350, width=150, height=20)
    file_label_entry.bind('<Return>', create_csv_file)

create_csv_button = ttk.Button(frame, text="Create CSV", command=create_csv_file)
create_csv_button.pack(pady=10)
create_csv_button.place(x=190, y=350, width=70, height=20)

img_label = tk.Label(frame)
img_label.pack()
img_label.place(x=520, y=130, width=150, height=170)

def resize_widgets(event):
    new_width = event.width
    new_height = event.height
    label.config(font=("Arial", int(new_height/15)))
    entry.place(x=30, y=int(new_height * 8), width=int(new_width * 8))
    file_label_entry.place(x=30, y=int(new_height * 0.9), width=int(new_width * 0.3))
    create_csv_button.place(x=int(new_width * 0.4), y=int(new_height * 0.9), width=int(new_width * 0.2), height=int(new_height * 0.05))
    result_label.place(x=30, y=int(new_height * 0.3), width=int(new_width * 0.3))
    button.place(x=int(new_width * 0.4), y=int(new_height * 0.2), width=int(new_width * 0.2), height=int(new_height * 0.05))
    img_label.place(x=int(new_width * 0.75), y=int(new_height * 0.2), width=int(new_width * 0.2), height=int(new_height * 0.4))

def save_attendance(doctors):
    filename = file_label_entry.get()
    current_date = datetime.now().strftime("%Y-%m-%d")
    directory = f'{current_date}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f'{directory}/{filename}', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        for doctor in doctors:
            if len(doctor) == 1:
                doctor.append('Absent')
            csv_writer.writerow(doctor)

def search_doctor(barcode):
    barcode = barcode.strip()
    with open('doctors.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        doctors = list(csv_reader)
    for row in doctors:
        if re.match(r'^' + re.escape(barcode) + r'$', row[0]):
            row.append('Present')
            save_attendance(doctors)
            display_image(barcode)
            return row
    return "Doctor not found!"

def search_action():
    barcode = entry.get()
    result = check_doctor(barcode)
    if result == "Re-enter":
        result_label.config(text="Re-enter: Barcode already scanned")
    elif isinstance(result, list):
        details = f"Name: {result[1]} {result[2]}, {result[3]}"
        result_label.config(text=f"Doctor found: {details}")
    else:
        result_label.config(text="Doctor not found")
    entry.delete(0, tk.END)

button = ttk.Button(frame, text="SEARCH", command=search_action)
button.pack()
button.place(x=235, y=90, width=60, height=20)

def display_details(row):
    details = f"Name: {row[1]} {row[2]}, {row[3]}"
    result_label.config(text=f"Doctor found: {details}")

def check_doctor(barcode):
    barcode = barcode.strip()
    if barcode in scanned_barcodes:
        result_label.config(text="Re-enter: Barcode already scanned")
        return "Re-enter"
    with open('doctors.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        doctors = list(csv_reader)
    for row in doctors:
        if re.match(r'^' + re.escape(barcode) + r'$', row[0]):
            if len(row) < 4:
                return ["N/A", "N/A", "N/A", "N/A"]
            row.append('Present')
            save_attendance(doctors)
            display_details(row)
            display_image(barcode)
            scanned_barcodes.add(barcode)
            return row
    return "Doctor not found"

def on_barcode_enter(event):
    search_action()

def on_key_release(event):
    value = entry.get()
    if len(value) == 12:
        search_action()
    elif not re.match(r'^\d{0,12}$', value):
        entry.delete(12, tk.END)

def display_image(barcode):
    try:
        img_path = f'images/{barcode}.png'
        if not os.path.exists(img_path):
            img_path = 'images/userpfp.png'
        img = Image.open(img_path)
        img = img.resize((150, 170), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        img_label.config(image=img)
        img_label.image = img
    except Exception as e:
        print(f"Error loading image: {e}")

def center_window(window):
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

root.after(0, center_window, root)
entry.bind('<Return>', on_barcode_enter)
entry.bind('<KeyRelease>', on_key_release)
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')
root.mainloop()
