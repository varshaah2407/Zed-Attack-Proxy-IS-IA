#Cipher Safe
import base64
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import user_password
import pyperclip
import json
import re
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_password():
    # Password Generator Project
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_password = [random.choice(letters) for _ in range(random.randint(8, 10))]
    numbers_password = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    symbols_password = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = letters_password + numbers_password + symbols_password
    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    entry_password.insert(0, password)


def save():
    email = entry_email.get()
    newPass = entry_password.get()
    website = entry_website.get()

    if email == "" or newPass == "" or website == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty.")

    else:
        master = simpledialog.askstring(title="Master Key", prompt="Enter master password:")

        result = user_password.encrypt(master,newPass)
        encrypted_password = result[0]
        salt = result[1]

        
        data_dict = {
            website: {
                "email": email,
                "password": encrypted_password,
                "salt": salt
            }
        }


        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(data_dict, file, indent=4)
        else:
            data.update(data_dict)

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_password.delete(0, END)


def search():
    website = entry_website.get()

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="No data found", message="Data list is empty.\n"
                                                            "Add any website information and then try searching.")
    else:
        if website in data:
            master = simpledialog.askstring(title="Master Password", prompt="Enter master password:")
            email = data[website]["email"]
            password = data[website]["password"]
            salt = data[website]["salt"]
            decrypted_password = user_password.decrypt(password, master, salt)           
            if decrypted_password:
                messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {decrypted_password}")
            else:
                messagebox.showerror(title="Error", message=f"Master password '{master}' is wrong")
        else:
            messagebox.showerror(title="No data found", message=f"Data does not exist under '{website}' name")


def password_check():
    password = entry_password.get()
    # calculating the length
    length_error = len(password) < 7

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"\W", password) is None

    # overall result
    strong = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )
    medium = not ( length_error or digit_error or uppercase_error or lowercase_error )
    if strong:
        messagebox.showinfo(title='Password Strength', message=f"Password: {password}\nStrength: Strong💪")
    elif medium:
        messagebox.showinfo(title='Password Strength', message=f"Password: {password}\nStrength: Medium🤓")
    else:
        messagebox.showinfo(title='Password Strength', message=f"Password: {password}\nStrength: Weak😟")




window = Tk()
window_icon = PhotoImage(file = "./window_final.png")
# window_icon = window_icon.zoom(4, 4)

window.iconphoto(False, window_icon)
window.title("CipherSafe")
window.config(padx=30, pady=30, background="#defcf9")

logo_img = PhotoImage(file="vault_bg_removed.png")
logo_img = logo_img.subsample(2, 2)  # Scale down the image by a factor of 10

canvas = Canvas(width=250, height=200, background="#defcf9")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# labels
label_website = Label(text="Website:", background="#defcf9")
label_website.grid(row=1, column=0, pady=7)

label_email = Label(text="Email/Username:", background="#defcf9")
label_email.grid(row=2, column=0, pady=7)

label_password = Label(text="Password:", background="#defcf9")
label_password.grid(row=3, column=0, pady=7)

# enteries
entry_website = Entry(width=21)
entry_website.grid(row=1, column=1, pady=7)
entry_website.focus()

entry_email = Entry(width=35)
entry_email.grid(row=2, column=1, columnspan=2, pady=7)

entry_password = Entry(width=21)
entry_password.grid(row=3, column=1, pady=7)

# buttons
button_password = Button(text="Generate Pass", command=generate_password)
button_password.grid(row=3, column=2, pady=7)

button_add = Button(text="Add", width=36, command=save)
button_add.grid(row=5, column=1, columnspan=2, pady=7)

button_search = Button(text="Search", command=search)
button_search.grid(row=1, column=2, pady=7)

button_strength = Button(text="Strength", command=password_check)
button_strength.grid(row=4, column=2, pady=4)

window.mainloop()
