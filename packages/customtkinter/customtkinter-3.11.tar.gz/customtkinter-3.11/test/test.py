import tkinter
import customtkinter
from PIL import Image
from PIL import ImageTk

root_tk = customtkinter.CTk()
root_tk.geometry("400x240")

def button_function():
    print("button pressed")

button = customtkinter.CTkButton(
        border_width=3,
        corner_radius=20,
        width=20,
        compound="bottom",
            master=root_tk,
            text="Testdfgd",
            image=ImageTk.PhotoImage(Image.open("test_images/bell.png").resize((30, 30))),
            command=button_function)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

button.config(state=tkinter.DISABLED)

root_tk.mainloop()