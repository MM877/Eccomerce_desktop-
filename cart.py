import tkinter as tk
from tkinter import Toplevel

def open_cart():
    cart_window = Toplevel(root)
    cart_window.title("My Cart")
    cart_window.geometry("400x300")
    tk.Label(cart_window, text="This is your cart page", font=("Arial", 16)).pack(pady=50)

# --- main window ---
root = tk.Tk()
root.title("Shop System")
root.geometry("800x600")

# --- cart button with image ---
cart_img = tk.PhotoImage(file="lock.png")  # put your cart.png inside images/
cart_button = tk.Button(root, image=cart_img, command=open_cart, bd=0, relief="flat")
cart_button.pack(side="top", anchor="ne", padx=10, pady=10)

# --- example content ---
tk.Label(root, text="Welcome to the Store!", font=("Arial", 20)).pack(pady=50)

root.mainloop()
