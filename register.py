from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json, os
import login

def register_page():
    global root
    root = Tk()

    root.geometry('1320x672')
    root.resizable(0, 0)
    root.title('Registration Page')

    # --- Load background image ---
    bgImage = ImageTk.PhotoImage(Image.open('background.jpg'))
    bgLabel = Label(root, image=bgImage)
    bgLabel.place(x=0, y=0)

    # --- Create left frame (form) ---
    frame1 = Frame(root, width=500, height=550, highlightbackground='#999966', highlightthickness=2, bg="white")
    frame1.place(x=100, y=70)

    # --- Registration Form Labels & Entries ---
    Label(frame1, text="Full Name", font=("Arial", 12, "bold"), bg="white").place(x=50, y=50)
    entry_name = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_name.place(x=50, y=80)

    Label(frame1, text="Email", font=("Arial", 12, "bold"), bg="white").place(x=50, y=130)
    entry_email = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_email.place(x=50, y=160)

    Label(frame1, text="Username", font=("Arial", 12, "bold"), bg="white").place(x=50, y=210)
    entry_username = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_username.place(x=50, y=240)

    Label(frame1, text="Password", font=("Arial", 12, "bold"), bg="white").place(x=50, y=290)
    entry_password = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid", show="*")
    entry_password.place(x=50, y=320)

    Label(frame1, text="Confirm Password", font=("Arial", 12, "bold"), bg="white").place(x=50, y=370)
    entry_cpassword = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid", show="*")
    entry_cpassword.place(x=50, y=400)


    """
    login link function
    """

    def open_login():
        root.destroy()
        login.login_page()

        
    # --- Save Data Function ---
    def save_data():
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        cpassword = entry_cpassword.get().strip()
        
        # Validation
        if not name or not email or not username or not password or not cpassword:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if password != cpassword:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        user_data = {
            "Full Name": name,
            "Email": email,
            "Username": username,
            "Password": password
        }
        
        # Save to JSON file
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                try:
                    data = json.load(file)
                except:
                    data = []
        else:
            data = []
        
        data.append(user_data)
        
        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)
        
        messagebox.showinfo("Success", "Registration Successful!")
        
        # Clear fields
        entry_name.delete(0, END)
        entry_email.delete(0, END)
        entry_username.delete(0, END)
        entry_password.delete(0, END)
        entry_cpassword.delete(0, END)

    # Register Button
    btn_register = Button(frame1, text="Register", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=20, height=2, relief="flat", cursor="hand2", command=save_data)
    btn_register.place(x=65, y=480)

    # --- Load lock icon (transparent PNG) ---
    lockImage = Image.open("lock.png").resize((180, 180))
    lockPhoto = ImageTk.PhotoImage(lockImage)

    lockLabel = Label(root, image=lockPhoto,background="#E9E7E7", borderwidth=0, highlightthickness=0, bg=None)
    lockLabel.place(x=840, y=230)

    # Add "Register Form" text under the lock icon
    titleLabel = Label(root, text="Register Form", font=("Arial", 30, "bold"), fg="#ffffff", bg="#000000")  
    titleLabel.place(x=800, y=420)


    # --- Switch to Login ---
    switch_button = Button(frame1, text="Already have account? Login", font=("Arial", 9), bg="white", fg="blue", command=open_login)
    switch_button.place(x=65, y=450)


    root.mainloop()
if __name__ == "__main__":
    register_page()

