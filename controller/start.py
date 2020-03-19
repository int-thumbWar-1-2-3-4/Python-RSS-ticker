import tkinter as tk
from view.main_view import MainView

root = tk.Tk()
app = MainView(master=root)
app.mainloop()