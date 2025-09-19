from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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
    try:
        bgImage = ImageTk.PhotoImage(Image.open('background.jpg'))
        bgLabel = Label(root, image=bgImage)
        bgLabel.place(x=0, y=0)
    except:
        root.configure(bg="#f0f0f0")  # Fallback background color

    # --- Create left frame (form) ---
    frame1 = Frame(root, width=500, height=600, highlightbackground='#999966', highlightthickness=2, bg="white")
    frame1.place(x=100, y=30)

    # --- Registration Form Labels & Entries ---
    Label(frame1, text="Full Name", font=("Arial", 12, "bold"), bg="white").place(x=50, y=20)
    entry_name = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_name.place(x=50, y=45)

    Label(frame1, text="Email", font=("Arial", 12, "bold"), bg="white").place(x=50, y=75)
    entry_email = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_email.place(x=50, y=100)

    Label(frame1, text="National ID", font=("Arial", 12, "bold"), bg="white").place(x=50, y=130)
    entry_ID = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_ID.place(x=50, y=155)

    Label(frame1, text="Password", font=("Arial", 12, "bold"), bg="white").place(x=50, y=185)
    entry_password = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid", show="*")
    entry_password.place(x=50, y=210)

    Label(frame1, text="Confirm Password", font=("Arial", 12, "bold"), bg="white").place(x=50, y=240)
    entry_cpassword = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid", show="*")
    entry_cpassword.place(x=50, y=265)

    Label(frame1, text="Governorate", font=("Arial", 12, "bold"), bg="white").place(x=50, y=295)
    entry_governorate = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_governorate.place(x=50, y=320)

    Label(frame1, text="Phone Number", font=("Arial", 12, "bold"), bg="white").place(x=50, y=350)
    entry_phone = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_phone.place(x=50, y=375)

    Label(frame1, text="Age", font=("Arial", 12, "bold"), bg="white").place(x=50, y=405)
    entry_age = Entry(frame1, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_age.place(x=50, y=430)

    # Gender dropdown - Fixed positioning
    Label(frame1, text="Gender", font=("Arial", 12, "bold"), bg="white").place(x=50, y=460)
    options = ["Male", "Female"]
    gender = ttk.Combobox(frame1, values=options, width=27, font=("Arial", 12))
    gender.set("Choose your gender")
    gender.place(x=50, y=485)

    # --- Login link function ---
    def open_login():
        root.destroy()
        login.login_page()

    # --- Validation Functions ---
    def validate_email(email):
        """Basic email validation"""
        return "@" in email and "." in email.split("@")[1]

    def validate_phone(phone):
        """Basic phone validation"""
        return phone.isdigit() and len(phone) >= 10

    def validate_age(age):
        """Age validation"""
        try:
            age_int = int(age)
            return 18 <= age_int <= 100
        except ValueError:
            return False

    def validate_id(national_id):
        """National ID validation"""
        return national_id.isdigit() and len(national_id) >= 10

    # --- Save Data Function ---
    def save_data():
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        ID = entry_ID.get().strip()
        password = entry_password.get().strip()
        cpassword = entry_cpassword.get().strip()
        governorate = entry_governorate.get().strip()
        phone = entry_phone.get().strip()
        age = entry_age.get().strip()
        selected_gender = gender.get()
        
        # Validation
        if not all([name, email, ID, password, cpassword, governorate, phone, age]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if selected_gender == "Choose your gender":
            messagebox.showerror("Error", "Please select your gender!")
            return
        
        if password != cpassword:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long!")
            return
        
        if not validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address!")
            return
        
        if not validate_phone(phone):
            messagebox.showerror("Error", "Please enter a valid phone number (digits only, minimum 10 digits)!")
            return
        
        if not validate_age(age):
            messagebox.showerror("Error", "Please enter a valid age (18-100)!")
            return
        
        if not validate_id(ID):
            messagebox.showerror("Error", "Please enter a valid National ID (digits only, minimum 10 digits)!")
            return
        
        # Check if user already exists
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                try:
                    existing_users = json.load(file)
                    for user in existing_users:
                        if user.get("Email") == email or user.get("ID") == ID:
                            messagebox.showerror("Error", "User with this email or ID already exists!")
                            return
                except json.JSONDecodeError:
                    existing_users = []
        else:
            existing_users = []
        
        user_data = {
            "Full Name": name,
            "Email": email,
            "ID": ID,
            "Password": password,
            "Governorate": governorate,
            "Phone": phone,
            "Age": int(age),
            "Gender": selected_gender,
        }
        
        # Save to JSON file
        existing_users.append(user_data)
        
        try:
            with open("users.json", "w") as file:
                json.dump(existing_users, file, indent=4)
            
            messagebox.showinfo("Success", "Registration Successful!")
            
            # Clear all fields
            entry_name.delete(0, END)
            entry_email.delete(0, END)
            entry_ID.delete(0, END)
            entry_password.delete(0, END)
            entry_cpassword.delete(0, END)
            entry_governorate.delete(0, END)
            entry_phone.delete(0, END)
            entry_age.delete(0, END)
            gender.set("Choose your gender")
            
            # Ask if user wants to login now
            if messagebox.askyesno("Login", "Would you like to login now?"):
                open_login()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save registration data: {str(e)}")

    # Register Button
    btn_register = Button(frame1, text="Register", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                         width=20, height=2, relief="flat", cursor="hand2", command=save_data)
    btn_register.place(x=50, y=520)

    # --- Load lock icon (with error handling) ---
    try:
        lockImage = Image.open("lock.png").resize((180, 180))
        lockPhoto = ImageTk.PhotoImage(lockImage)
        lockLabel = Label(root, image=lockPhoto, background="#E9E7E7", borderwidth=0, highlightthickness=0)
        lockLabel.place(x=840, y=230)
        
        # Keep reference to prevent garbage collection
        lockLabel.image = lockPhoto
    except FileNotFoundError:
        # Create a text placeholder if image not found
        lockLabel = Label(root, text="🔐", font=("Arial", 100), bg="#E9E7E7", fg="#666")
        lockLabel.place(x=890, y=280)

    # Add "Register Form" text under the lock icon
    titleLabel = Label(root, text="Register Form", font=("Arial", 30, "bold"), fg="#ffffff", bg="#000000")  
    titleLabel.place(x=800, y=420)

    # --- Switch to Login ---
    switch_button = Button(frame1, text="Already have account? Login", font=("Arial", 10), 
                          bg="white", fg="blue", bd=0, cursor="hand2", command=open_login)
    switch_button.place(x=300, y=560)

    # Bind Enter key to register
    def on_enter(event):
        save_data()
    
    root.bind('<Return>', on_enter)

    root.mainloop()

if __name__ == "__main__":
    register_page()