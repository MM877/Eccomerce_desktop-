from tkinter import *
from PIL import Image, ImageTk
import register

def open_register():
    root.destroy()
    register.register_page()

def login_page():
    global root
    root = Tk()
    root.geometry('1320x672')
    root.resizable(0, 0)
    root.title('Login Page')

    # --- Load background image ---
    bgImage = ImageTk.PhotoImage(Image.open('background.jpg'))
    bgLabel = Label(root, image=bgImage)
    bgLabel.image = bgImage
    bgLabel.place(x=0, y=0)

    # --- Create left frame (form) ---
    frame1 = Frame(root, width=500, height=350, highlightbackground='#999966', highlightthickness=2, bg="white")
    frame1.place(x=100, y=150)

    # --- Load lock icon ---
    lockImage = Image.open("lock.png").resize((180, 180))
    lockPhoto = ImageTk.PhotoImage(lockImage)
    lockLabel = Label(root, image=lockPhoto,background="#E9E7E7", borderwidth=0, highlightthickness=0, bg=None)
    lockLabel.place(x=840, y=230)
    lockLabel.image = lockPhoto
    

    # --- Add "Login Form" text ---
    titleLabel = Label(root, text="Login Form", font=("Arial", 30, "bold"), fg="#ffffff", bg="#000000")  
    titleLabel.place(x=820, y=420)

    # --- Form fields ---
    Label(frame1, text="Username:", font=("Arial", 14), bg="white").place(x=50, y=50)
    username_entry = Entry(frame1, font=("Arial", 14), width=25, bd=2)
    username_entry.place(x=180, y=50)

    Label(frame1, text="Password:", font=("Arial", 14), bg="white").place(x=50, y=120)
    password_entry = Entry(frame1, font=("Arial", 14), width=25, bd=2, show="*")
    password_entry.place(x=180, y=120)

    # --- Buttons ---
    login_button = Button(frame1, text="Login", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=12)
    login_button.place(x=90, y=220)

    clear_button = Button(frame1, text="Clear", font=("Arial", 14, "bold"), bg="#f44336", fg="white", width=12)
    clear_button.place(x=260, y=220)

    # --- Switch to Register ---
    switch_button = Button(frame1, text="Create Account", font=("Arial", 12), bg="white", fg="blue", command=open_register)
    switch_button.place(x=180, y=280)

    root.mainloop()

if __name__ == "__main__":
    login_page()
