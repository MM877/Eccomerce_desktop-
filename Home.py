from tkinter import *
from PIL import Image, ImageTk
import json, os
from products_page import products_page   

def load_categories():
    if os.path.exists("products.json"):
        with open("products.json", "r") as f:
            try:
                data = json.load(f)
                categories = list({item["category"] for item in data})
                return categories
            except:
                return []
    return []

def categories_page():
    root = Tk()
    root.geometry("1320x672")
    root.resizable(0, 0)
    root.title("Categories")

    bgImage = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
    bgLabel = Label(root, image=bgImage)
    bgLabel.image = bgImage
    bgLabel.place(x=0, y=0)

    categories = load_categories()

    positions = [(30,30), (1050,30), (30,500), (1050,500)]

    for i, cat in enumerate(categories[:4]):
        btn = Button(
            root,
            text=cat,
            font=("Arial", 18, "bold"),
            width=12,
            height=5,
            bg="#4CAF50",
            fg="white",
            relief="raised",
            cursor="hand2",
            command=lambda c=cat: products_page(c)   # 👈 Open products
        )
        btn.place(x=positions[i][0], y=positions[i][1])

    root.mainloop()

if __name__ == "__main__":
    categories_page()
