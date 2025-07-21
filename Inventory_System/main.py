from Inventory_System.Operantions_Center.system import System
from Inventory_System.Operantions_Center.app import InventoryApp
import tkinter as tk

if __name__ == "__main__":

    root = tk.Tk()
    system = System()

    app = InventoryApp(root, system)
    root.mainloop()