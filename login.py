from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import register
import json
import os

def open_register():
    root.destroy()
    register.register_page()

def login_user(username, password):
    # --- Admin fixed login ---
    if username == "admin@gmail.com" and password == "admin123":
        messagebox.showinfo("Admin Login", "Welcome Admin!")
        root.destroy()
        return "admin"

    # --- Regular users from users.json ---
    if not os.path.exists("users.json"):
        messagebox.showerror("Error", "No registered users found! Please register first.")
        return None
    
    with open("users.json", "r") as file:
        try:
            users = json.load(file)
        except:
            users = []

    for user in users:
        if (username == user.get("Username") or username == user.get("Email")) and password == user.get("Password"):
            messagebox.showinfo("Success", f"Welcome {user.get('Full Name', 'User')}!")
            root.destroy()
            return "user"
    
    messagebox.showerror("Error", "Invalid Username/Email or Password")
    return None

def login_page():
    global root
    root = Tk()
    root.geometry('1320x672')
    root.resizable(0, 0)
    root.title('Login Page')

    bgImage = ImageTk.PhotoImage(Image.open('background.jpg'))
    bgLabel = Label(root, image=bgImage)
    bgLabel.image = bgImage
    bgLabel.place(x=0, y=0)

    frame1 = Frame(root, width=500, height=350, highlightbackground='#999966', highlightthickness=2, bg="white")
    frame1.place(x=100, y=150)

    lockImage = Image.open("lock.png").resize((180, 180))
    lockPhoto = ImageTk.PhotoImage(lockImage)
    lockLabel = Label(root, image=lockPhoto, background="#E9E7E7", borderwidth=0, highlightthickness=0)
    lockLabel.place(x=840, y=230)
    lockLabel.image = lockPhoto

    titleLabel = Label(root, text="Login Form", font=("Arial", 30, "bold"), fg="#ffffff", bg="#000000")  
    titleLabel.place(x=820, y=420)

    Label(frame1, text="Username/Email:", font=("Arial", 14), bg="white").place(x=50, y=50)
    username_entry = Entry(frame1, font=("Arial", 14), width=25, bd=2)
    username_entry.place(x=200, y=50)

    Label(frame1, text="Password:", font=("Arial", 14), bg="white").place(x=50, y=120)
    password_entry = Entry(frame1, font=("Arial", 14), width=25, bd=2, show="*")
    password_entry.place(x=200, y=120)

    result = {"type": None}

    def handle_login():
        result["type"] = login_user(username_entry.get(), password_entry.get())

    login_button = Button(
        frame1, text="Login", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=12,
        command=handle_login
    )
    login_button.place(x=90, y=220)

    clear_button = Button(
        frame1, text="Clear", font=("Arial", 14, "bold"), bg="#f44336", fg="white", width=12,
        command=lambda: [username_entry.delete(0, END), password_entry.delete(0, END)]
    )
    clear_button.place(x=260, y=220)

    switch_button = Button(
        frame1, text="Create Account", font=("Arial", 12), bg="white", fg="blue",
        command=open_register
    )
    switch_button.place(x=180, y=280)

    root.mainloop()
    return result["type"]

if __name__ == "__main__":
    user_type = login_page()
    print("Logged in as:", user_type)
