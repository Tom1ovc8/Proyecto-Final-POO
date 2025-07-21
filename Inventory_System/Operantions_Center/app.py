import tkinter as tk
from tkinter import (
    filedialog, messagebox, Toplevel, StringVar, OptionMenu, ttk
)

from Inventory_System.Operantions_Center.system import System
from Inventory_System.Operantions_Center.extracts import Extracts
from Inventory_System.Products.product import Product
from Inventory_System.Products.state import State
from Inventory_System.People.supplier import Supplier
from Inventory_System.People.customer import Customer
from Inventory_System.Transactions.bills import Bill
from Inventory_System.Transactions.payment import Card, Cash
from Inventory_System.Transactions.movements import Movement

class InventoryApp:
    def __init__(self, root, system):
        self.root = root
        root.title("Inventory Management System")
        self.system = system

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)

        buttons = [
            ("📂 Load JSON archive", self.load_json),
            ("💾 Export to JSON archive", self.export_to_json),
            ("➕ Add Product", self.add_product_method),
            ("📋 Inventory Report", self.generate_inventory_pdf),
            ("🔄 Add Movement", self.add_movement_dialog),
            ("🧾 Cash Register", self.create_bill_dialog),
            ("📜 Customer/Supplier History", self.generate_actor_history),
            ("📤 Export Bill", self.export_bill_dialog),
            ("📈 Sales Summary", self.generate_sales_summary),
            ("📦 Restock Suggestions", self.show_restock_suggestions),
            ("🚪 Quit", root.quit)
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(
                main_frame, text=text, command=command
            ).pack(pady=6, fill="x")

    def load_json(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")]
        )
        if filepath:
            try:
                System.load_full_backup(self.system, filepath)
                messagebox.showinfo(
                    "Success", "JSON archive has been loaded."
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Couldn't load the archive:\n{e}"
                )

    def generate_inventory_pdf(self):
        try:
            System.export_inventory_pdf(self.system)
            messagebox.showinfo(
                "Success", 
                "Report has been generated as 'inventory_report.pdf'"
            )
        except Exception as e:
            messagebox.showerror(
                "Error", f"Couldn't generate the report:\n{e}"
            )

    def generate_actor_history(self):
        actor_id = simple_input_dialog(
            "Join the actor ID (customer/supplier):"
        )
        if not actor_id:
            return
        try:
            System.export_actor_history_pdf(self.system, actor_id)
            messagebox.showinfo("Success", f"History has been generated.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Couldn't generate the history:\n{e}"
            )

    def add_product_method(self):
        dialog = Toplevel(self.root)
        dialog.title("Add Product")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)

        fields = ["Name", "Category", "Code", "Price", "Initial Amount"]
        entries = {}
        for field in fields:
            ttk.Label(
                main_frame, text=field).pack(padx=10, pady=2, anchor="w"
            )
            entry = ttk.Entry(main_frame)
            entry.pack(padx=10, pady=2, fill="x")
            entries[field] = entry

        ttk.Label(
            main_frame, text="Select State type:"
        ).pack(pady=5, anchor="w")
        state_type = tk.StringVar(value="condition")
        ttk.Radiobutton(
            main_frame, text="State", variable=state_type, value="condition"
        ).pack(anchor="w")
        ttk.Radiobutton(
            main_frame, text="Expiration Date", 
            variable=state_type, value="date"
        ).pack(anchor="w")

        state_container = ttk.Frame(main_frame)
        state_container.pack(pady=5, fill="x")

        condition_frame = ttk.Frame(state_container)
        ttk.Label(condition_frame, text="Condition:").pack(pady=2, anchor="w")
        condition_entry = ttk.Entry(condition_frame)
        condition_entry.pack(pady=2, fill="x")

        expiration_frame = ttk.Frame(state_container)
        for label_text in ["Exp. Year:", "Exp. Month:", "Exp. Day:"]:
            ttk.Label(
                expiration_frame, text=label_text
            ).pack(pady=2, anchor="w")
            ttk.Entry(expiration_frame).pack(pady=2, fill="x")
        year_entry, month_entry, day_entry = (
            expiration_frame.winfo_children()[1::2]
        )

        def update_state_fields():
            if state_type.get() == "condition":
                expiration_frame.pack_forget()
                condition_frame.pack(fill="x")
            else:
                condition_frame.pack_forget()
                expiration_frame.pack(fill="x")

        update_state_fields()
        state_type.trace_add("write", lambda *args: update_state_fields())

        ttk.Label(
            main_frame, text="Select Supplier type:"
        ).pack(pady=5, anchor="w")
        supplier_option = tk.StringVar(value="existent")
        ttk.Radiobutton(
            main_frame, text="Existent", 
            variable=supplier_option, value="existent"
        ).pack(anchor="w")
        ttk.Radiobutton(
            main_frame, text="New", variable=supplier_option, value="new"
        ).pack(anchor="w")

        supplier_container = ttk.Frame(main_frame)
        supplier_container.pack(fill="x")

        existing_supplier_frame = ttk.Frame(supplier_container)
        ttk.Label(
            existing_supplier_frame, text="Select existent supplier:"
        ).pack(anchor="w")
        supplier_var = tk.StringVar()

        if self.system.suppliers:
            supplier_names = [s.name for s in self.system.suppliers.values()]
            supplier_var.set(supplier_names[0])
            supplier_menu = ttk.OptionMenu(
                existing_supplier_frame, supplier_var,
                supplier_names[0],*supplier_names
            )
        else:
            supplier_var.set("There's not suppliers")
            supplier_menu = ttk.OptionMenu(
                existing_supplier_frame, supplier_var,
                "There's not suppliers"
            )
            supplier_menu.state(["disabled"])
        supplier_menu.pack(fill="x")
        existing_supplier_frame.pack(pady=5, fill="x")

        new_supplier_frame = ttk.Frame(supplier_container)
        for label in ["New supplier name:", "New supplier contact:"]:
            ttk.Label(new_supplier_frame, text=label).pack(anchor="w")
            ttk.Entry(new_supplier_frame).pack(fill="x", pady=2)
        new_supplier_name, new_supplier_contact = (
            new_supplier_frame.winfo_children()[1::2]
        )

        def toggle_supplier_frames():
            if supplier_option.get() == "existent":
                new_supplier_frame.pack_forget()
                existing_supplier_frame.pack(pady=5, fill="x")
            else:
                existing_supplier_frame.pack_forget()
                new_supplier_frame.pack(pady=5, fill="x")

        supplier_option.trace_add(
            "write", lambda *args: toggle_supplier_frames()
        )

        def submit():
            try:
                name = entries["Name"].get().strip()
                category = entries["Category"].get().strip()
                code = entries["Code"].get().strip()
                price_str = entries["Price"].get().strip()
                amount_str = entries["Initial Amount"].get().strip()

                if (
                    not name or not category or not code or
                    not price_str or not amount_str
                ):
                    raise ValueError("All fields must be filled")

                try:
                    price = float(price_str)
                    amount = int(amount_str)
                    if price <= 0 or amount <= 0:
                        raise ValueError(
                            "Price and Amount must be bigger than zero"
                        )
                except ValueError:
                    raise ValueError("Price and Amount must be numeric.")

                if state_type.get() == "condition":
                    if (
                        not condition_entry or
                        not condition_entry.get().strip()
                    ):
                        raise ValueError("You must fill the codition.")
                    state = State(condition=condition_entry.get().strip())
                else:
                    if not year_entry or not month_entry or not day_entry:
                        raise ValueError("You must fill the entire date.")
                    try:
                        state_tuple = (
                            int(year_entry.get().strip()),
                            int(month_entry.get().strip()),
                            int(day_entry.get().strip())
                        )
                        state = State(expiration_date=state_tuple)
                    except ValueError:
                        raise ValueError(
                            "Date fields must be valid numbers."
                        )

                if (
                    supplier_option.get() == "existent" and
                    self.system.suppliers
                ):
                    supplier = next(
                        (
                            s for s in self.system.suppliers.values() 
                            if s.name == supplier_var.get()
                         ), None
                    )
                else:
                    supplier_name = new_supplier_name.get().strip()
                    supplier_contact = new_supplier_contact.get().strip()
                    if not supplier_name or not supplier_contact:
                        raise ValueError(
                            "You must enter the supplier name and contact."
                        )
                    if not supplier_contact.isdigit():
                        raise ValueError(
                            "The contact number must be numeric only"
                        )
                    
                    existing = [
                        supplier for supplier in self.system.suppliers.values() 
                        if (
                            supplier.name == supplier_name and
                            supplier.contact == supplier_contact
                        )
                    ]
                    if existing:
                        supplier = existing[0]
                    else:
                        supplier = Supplier(supplier_name, supplier_contact)
                        self.system.add_supplier(supplier)

                product = Product(name, category, code, price, state)
                self.system.entry_record(
                    product, amount, supplier, reason="New add"
                )
                messagebox.showinfo("Success", f"Product '{name}' added.")
                dialog.destroy()

            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror(
                    "Error", f"Couldn't add the product:\n{str(e)}"
                )

        ttk.Button(
            main_frame, text="Add Product", command=submit
        ).pack(pady=10)

    def export_to_json(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Backup"
        )
        if filepath:
            try:
                self.system.export_full_system(filepath)
                messagebox.showinfo(
                    "Success", f"Backup saved in:\n{filepath}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't export:\n{e}")

    def add_movement_dialog(self):
        if not self.system.records:
            messagebox.showwarning(
                "No products available", 
                "Unable to register movements, no products availables"
            )
            return
         
        dialog = tk.Toplevel()
        dialog.title("Register Movement")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame, text="Select Movement type:"
        ).pack(pady=5, anchor="w")
        movement_type = tk.StringVar(value="in")
        ttk.Radiobutton(
            main_frame, text="In", variable=movement_type, value="in", 
            command=lambda: update_actor_menu()
        ).pack(anchor="w")
        ttk.Radiobutton(
            main_frame, text="Out", variable=movement_type, value="out", 
            command=lambda: update_actor_menu()
        ).pack(anchor="w")

        ttk.Label(main_frame, text="Select product:").pack(pady=5, anchor="w")
        product_var = tk.StringVar(main_frame)
        if self.system.records:
            product_var.set(
                next(iter(self.system.records.values())).product.name
            )
        product_menu = ttk.OptionMenu(
            main_frame, product_var, 
            *[record.product.name for record in self.system.records.values()]
        )
        product_menu.pack(pady=5, fill="x")

        ttk.Label(main_frame, text="Amount:").pack(pady=5, anchor="w")
        quantity_entry = ttk.Entry(main_frame)
        quantity_entry.pack(pady=5, fill="x")

        ttk.Label(
            main_frame, text="Reason of the movement:"
        ).pack(pady=5, anchor="w")
        reason_entry = ttk.Entry(main_frame)
        reason_entry.pack(pady=5, fill="x")

        ttk.Label(main_frame, text="Type actor:").pack(pady=5, anchor="w")
        actor_option = tk.StringVar(value="existent")
        ttk.Radiobutton(
            main_frame, text="Existent", variable=actor_option, value="existent", 
            command=lambda: toggle_actor_fields()
        ).pack(anchor="w")
        ttk.Radiobutton(
            main_frame, text="New", variable=actor_option, value="new", 
            command=lambda: toggle_actor_fields()
        ).pack(anchor="w")

        actor_container = ttk.Frame(main_frame)
        actor_container.pack(pady=5, fill="x")

        existing_actor_frame = ttk.Frame(actor_container)
        actor_var = tk.StringVar(existing_actor_frame)
        actor_label = ttk.Label(
            existing_actor_frame, text="Select existent actor:"
        )
        actor_menu = ttk.OptionMenu(existing_actor_frame, actor_var, "")
        actor_label.pack(pady=5)
        actor_menu.pack(pady=5, fill="x")

        new_actor_frame = ttk.Frame(actor_container)
        new_actor_name_label = ttk.Label(
            new_actor_frame, text="New actor name:"
        )
        new_actor_contact_label = ttk.Label(
            new_actor_frame, text="New actor contact/id:"
        )
        new_actor_name_entry = ttk.Entry(new_actor_frame)
        new_actor_contact_entry = ttk.Entry(new_actor_frame)

        new_actor_name_label.pack(pady=3)
        new_actor_name_entry.pack(pady=3, fill="x")
        new_actor_contact_label.pack(pady=3)
        new_actor_contact_entry.pack(pady=3, fill="x")

        def toggle_actor_fields():
            existing_actor_frame.pack_forget()
            new_actor_frame.pack_forget()

            if actor_option.get() == "existent":
                existing_actor_frame.pack(pady=5, fill="x")
            else:
                new_actor_frame.pack(pady=5, fill="x")

        def update_actor_menu():
            if movement_type.get() == "in":
                options = [s.name for s in self.system.suppliers.values()]
            else:
                options = [c.name for c in self.system.customers.values()]

            for widget in existing_actor_frame.winfo_children():
                widget.destroy()

            ttk.Label(
                existing_actor_frame, text="Select existent actor:"
            ).pack(pady=2, anchor="w")

            if options:
                actor_var.set(options[0])
                new_menu = ttk.OptionMenu(
                    existing_actor_frame, actor_var, options[0], *options
                )
            else:
                actor_var.set("No actors available")
                new_menu = ttk.OptionMenu(
                    existing_actor_frame, actor_var, "No actors available"
                )
                new_menu.state(["disabled"])
            
            new_menu.pack(fill="x")
            toggle_actor_fields()

        update_actor_menu()
        actor_option.trace_add("write", lambda *args: toggle_actor_fields())

        def register_movement():
            try:
                if (
                    not quantity_entry.get().isdigit() or 
                    int(quantity_entry.get()) <= 0
                ):
                    raise ValueError("The amount must be positive.")
                if not reason_entry.get().strip():
                    raise ValueError("You have to enter a reason.")

                product_name = product_var.get()
                product = next(
                    r.product for r in self.system.records.values() 
                    if r.product.name == product_name
                )
                cantidad = int(quantity_entry.get())
                reason = reason_entry.get().strip()

                if movement_type.get() == "in":
                    if actor_option.get() == "existent":
                        actor = next(
                            (
                                s for s in self.system.suppliers.values() 
                                if s.name == actor_var.get()
                             ), None
                        )
                        if not actor:
                            raise ValueError(
                                "The supplier selected is invalid."
                            )
                    else:
                        name = new_actor_name_entry.get().strip()
                        contact = new_actor_contact_entry.get().strip()
                        if not name or not contact:
                            raise ValueError(
                                "Enter the new supplier name and contact."
                            )
                        actor = Supplier(name, contact)
                        self.system.add_supplier(actor)

                    self.system.restock(
                        product._code, cantidad, actor, reason
                    )

                else:
                    if actor_option.get() == "existent":
                        actor = next(
                            (
                                c for c in self.system.customers.values() 
                                if c.name == actor_var.get()
                             ), None
                        )
                        if not actor:
                            raise ValueError(
                                "The customer selected is invalid."
                            )
                    else:
                        name = new_actor_name_entry.get().strip()
                        contact = new_actor_contact_entry.get().strip()
                        if not name or not contact:
                            raise ValueError(
                                "Enter the new customer name and id."
                            )
                        actor = Customer(name, contact)
                        self.system.add_customer(actor)

                    self.system.make_sale(
                        product._code, cantidad, actor, reason
                    )

                messagebox.showinfo("Success", "Movement registered.")
                dialog.destroy()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Couldn't register the movement:\n{e}"
                )

        ttk.Button(
            main_frame, text="Register", command=register_movement
        ).pack(pady=15, fill="x")

    def create_bill_dialog(self):
        if not self.system.records:
            messagebox.showwarning(
                "No products available", 
                "No registered products, it's not possible to create a bill."
            )
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Create a bill")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=12)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Select the actor type:").pack(pady=5)
        actor_type = tk.StringVar(value="customer")
        ttk.Radiobutton(
            main_frame, text="Customer", variable=actor_type, 
            value="customer", command=lambda: update_actor_fields()
        ).pack()
        ttk.Radiobutton(
            main_frame, text="Supplier", variable=actor_type, 
            value="supplier", command=lambda: update_actor_fields()
        ).pack()

        actor_mode = tk.StringVar(value="existent")
        ttk.Label(
            main_frame, text="Choose actor: existing or new?"
        ).pack(pady=5)
        ttk.Radiobutton(
            main_frame, text="Existent", variable=actor_mode, 
            value="existent", command=lambda: update_actor_fields()
        ).pack()
        ttk.Radiobutton(
            main_frame, text="New", variable=actor_mode, value="new", 
            command=lambda: update_actor_fields()
        ).pack()

        actor_frame = ttk.Frame(main_frame)
        actor_frame.pack(pady=10, fill="x")
        existing_actor_frame = ttk.Frame(actor_frame)
        new_actor_frame = ttk.Frame(actor_frame)

        actor_var = tk.StringVar()
        new_actor_name = None
        new_actor_contact = None

        def update_actor_fields():
            for widget in existing_actor_frame.winfo_children():
                widget.destroy()
            for widget in new_actor_frame.winfo_children():
                widget.destroy()

            existing_actor_frame.pack_forget()
            new_actor_frame.pack_forget()

            actors_dict = (
                self.system.customers 
                if actor_type.get() == "customer" else self.system.suppliers
            )

            if actor_mode.get() == "existent":
                existing_actor_frame.pack()
                ttk.Label(
                    existing_actor_frame, text="Select an existent actor:"
                ).pack()
                if actors_dict:
                    actor_names = [a.name for a in actors_dict.values()]
                    actor_var.set(actor_names[0])
                    actor_menu = ttk.OptionMenu(
                        existing_actor_frame, actor_var, 
                        actor_names[0], *actor_names
                    )
                else:
                    actor_var.set("No actors available")
                    actor_menu = ttk.OptionMenu(
                        existing_actor_frame, actor_var, "No actors available"
                    )
                    actor_menu.state(["disabled"])
                actor_menu.pack()
            else:
                new_actor_frame.pack()
                ttk.Label(new_actor_frame, text="New actor name:").pack()
                nonlocal_new_name = ttk.Entry(new_actor_frame)
                nonlocal_new_name.pack(fill="x")
                ttk.Label(
                    new_actor_frame, text="New actor contact/id:"
                ).pack()
                nonlocal_new_contact = ttk.Entry(new_actor_frame)
                nonlocal_new_contact.pack(fill="x")

                nonlocal new_actor_name, new_actor_contact
                new_actor_name = nonlocal_new_name
                new_actor_contact = nonlocal_new_contact

        update_actor_fields()
        
        ttk.Label(main_frame, text="Add products:").pack(pady=4)
        manual_frame = ttk.Frame(main_frame)
        manual_frame.pack(pady=4)

        ttk.Label(manual_frame, text="Code:").grid(row=0, column=0)
        code_entry = ttk.Entry(manual_frame)
        code_entry.grid(row=0, column=1)

        ttk.Label(manual_frame, text="Amount:").grid(row=0, column=2)
        qty_entry = ttk.Entry(manual_frame)
        qty_entry.grid(row=0, column=3)

        items = []

        columns = ("Product", "Amount", "Price")
        tree = ttk.Treeview(
            main_frame, columns=columns, show="headings", height=7
        )
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(pady=8)

        def add_manual_item():
            code = code_entry.get().strip()
            qty = qty_entry.get().strip()
            if not code or not qty:
                messagebox.showerror("Error", "Complete all the fields.")
                return
            if code not in self.system.records:
                messagebox.showerror(
                    "Error", f"Product {code} has not found in inventory."
                )
                return
            try:
                qty = int(qty)
            except ValueError:
                messagebox.showerror("Error", "Amount must be numeric.")
                return

            product = self.system.records[code].product
            price = product._price
            items.append((product, qty))
            tree.insert("", "end", values=(product.name, qty, price))
            code_entry.delete(0, tk.END)
            qty_entry.delete(0, tk.END)

        ttk.Button(
            manual_frame, text="Add", command=add_manual_item
        ).grid(row=0, column=6, padx=5)

        ttk.Label(main_frame, text="Pending Movements:").pack(pady=5)
        pending_listbox = tk.Listbox(
            main_frame, selectmode=tk.EXTENDED, width=70, height=4
        )
        pending_listbox.pack()

        pending_movements = []

        def update_pending_movements():
            nonlocal pending_movements
            pending_listbox.delete(0, tk.END)

            actors_dict = (
                self.system.customers 
                if actor_type.get() == "customer" else self.system.suppliers
            )

            actor_obj = next((a for a in actors_dict.values() 
                            if a.name == actor_var.get()), None)

            if actor_obj:
                pending_movements = [
                    m for m in self.system.movements
                    if m.actor == actor_obj and 
                    getattr(m, "bill_id", None) is None
                ]
                for idx, mov in enumerate(pending_movements):
                    text = (
                        f"{idx+1}. {mov.product.name} x{mov.amount} — "
                        f"{mov.date.strftime('%Y-%m-%d')}"
                    )
                    pending_listbox.insert(tk.END, text)
            else:
                pending_movements = []

        actor_var.trace_add("write", lambda *args: update_pending_movements())
        update_pending_movements()

        ttk.Label(main_frame, text="Payment Method:").pack(pady=5)
        payment_method = tk.StringVar(value="cash")
        ttk.Radiobutton(
            main_frame, text="Cash", variable=payment_method, value="cash"
        ).pack()
        ttk.Radiobutton(
            main_frame, text="Card", variable=payment_method, value="card"
        ).pack()

        payment_frame = ttk.Frame(main_frame)
        payment_frame.pack(pady=5)

        payment_frame.cash_entry_ = None
        payment_frame.card_entry_ = None

        def update_payment_fields():
            for widget in payment_frame.winfo_children():
                widget.destroy()
            if payment_method.get() == "cash":
                ttk.Label(
                    payment_frame, text="Amount delivered:"
                ).pack(side="left")
                cash_entry = ttk.Entry(payment_frame)
                cash_entry.pack(side="left")
                payment_frame.cash_entry_ = cash_entry
                payment_frame.card_entry_ = None
            else:
                ttk.Label(
                    payment_frame, text="Card Number (4 last numbers):"
                ).pack(side="left")
                card_entry = ttk.Entry(payment_frame)               
                card_entry.pack(side="left")
                payment_frame.card_entry_ = card_entry
                payment_frame.cash_entry_ = None

        payment_method.trace_add(
            "write", lambda *args: update_payment_fields()
        )
        update_payment_fields()

        def submit():
            try:
                if actor_mode.get() == "existent":
                    if (
                        actor_var.get() and 
                        actor_var.get() != "It's not actors available"
                    ):
                        actors_dict = (
                            self.system.customers 
                            if actor_type.get() == "customer" 
                            else self.system.suppliers
                        )
                        actor = next(
                            (
                                a for a in actors_dict.values() 
                                if a.name == actor_var.get()
                             ), None
                        )
                    else:
                        raise ValueError("You must select a valid actor.")
                else:
                    actor_name = new_actor_name.get().strip()
                    actor_contact = new_actor_contact.get().strip()
                    if not actor_name or not actor_contact:
                        raise ValueError(
                            "Enter the new actor's information."
                        )
                    actor = (
                        Customer(actor_name, actor_contact) 
                        if actor_type.get() == "customer" 
                        else Supplier(actor_name, actor_contact)
                        )

                manual_movements = []
                for product, qty in items:
                    manual_movements.append(
                        Movement(product, qty, actor, "Manual sell")
                    )

                selected_indexes = pending_listbox.curselection()
                selected_pending = [
                    pending_movements[i] for i in selected_indexes
                ]

                all_movements = manual_movements + selected_pending
                if not all_movements:
                    raise ValueError(
                        "At least one movement is required for billing."
                    )

                total = sum(
                    m.product._price * m.amount for m in all_movements
                )
                if payment_method.get() == "cash":
                    cash_entry = payment_frame.cash_entry_
                    if not cash_entry:
                        raise ValueError("Cash entry not found.")
                    payment = Cash(float(cash_entry.get().strip()))
                else:
                    card_entry = payment_frame.card_entry_
                    if not card_entry:
                        raise ValueError("Card entry not found.")
                    num = card_entry.get().strip()
                    if not num.isdigit() or len(num) != 4:
                        raise ValueError("Card number must be 4 digits.")
                    payment = Card(num, "***")

                if not payment.pay(total):
                    raise ValueError("Insufficient payment.")

                if actor_mode.get() == "new":
                    if actor_type.get() == "customer":
                        self.system.add_customer(actor)
                    else:
                        self.system.add_supplier(actor)

                for movement in manual_movements:
                    self.system.add_movement(movement)
 
                bill = self.system.create_bill(actor, all_movements, payment)
                if bill is None:
                    raise RuntimeError("Failed to create bill")

                self.system.export_bill_pdf(
                    bill._bill_id, f"Bill_{bill.entity.name}.pdf"
                )

                messagebox.showinfo(
                    "Success", f"Bill created with ID: {bill._bill_id}"
                )
                dialog.destroy()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Couldn't create the bill:\n{str(e)}"
                )

        ttk.Button(
            main_frame, text="Create bill", command=submit
        ).pack(pady=10)

    def export_bill_dialog(self):
        bill_id = simple_input_dialog("Enter the ID of the bill:")
        if bill_id not in self.system.bills:
            messagebox.showerror(
                "Error", f"No bill exists with ID: {bill_id}"
            )
            return
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
            )
            if not filename:
                return
            self.system.export_bill_pdf(bill_id, filename)
            messagebox.showinfo("Success", f"Bill exported as:\n{filename}")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Couldn't export the bill:\n{str(e)}"
            )

    def generate_sales_summary(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Sales Summary")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=12)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame, text="Do you want to generate for a specific product?"
        ).pack(padx=10, pady=5)

        product_code_var = tk.StringVar()
        ttk.Entry(
            main_frame, textvariable=product_code_var
        ).pack(padx=10, pady=5)
        ttk.Label(
            main_frame, text="(Let it blank to generate the general report)"
        ).pack(pady=5)

        def submit():
            product_code = product_code_var.get().strip() or None
            if not self.system.records:
                messagebox.showerror(
                    "Error", "There're no registered products in the system."
                )
                return

            if product_code:
                codes = {m.product._code for m in self.system.movements}
                if product_code not in codes:
                    messagebox.showerror(
                        "Error", 
                        f"The product code '{product_code}' doesn't exist."
                    )
                    return
            try:
                self.system.export_sales_summary_pdf(
                    filename="sales_summary.pdf", product_code=product_code
                )
                messagebox.showinfo(
                    "Success", "Summary generated in 'sales_summary.pdf'"
                )
                dialog.destroy()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Couldn't generate the summary:\n{e}"
                )

        ttk.Button(main_frame, text="Generate", command=submit).pack(pady=10)

    def show_restock_suggestions(self):
        suggestions = self.system.restock_suggestions()

        if not suggestions:
            messagebox.showinfo("Info", "There are no restock suggestions.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Restock Suggestions")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame, text="Low-Stock Products"
        ).grid(row=0, column=0, columnspan=2, pady=(0,15))

        cols = ("Code", "Product", "Current", "Minimum")
        tree = ttk.Treeview(
            main_frame, columns=cols, show="headings", style="Treeview"
        )
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center")
        tree.grid(row=1, column=0, sticky="nsew")

        sb = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=sb.set)
        sb.grid(row=1, column=1, sticky="ns")

        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        for item in suggestions:
            tree.insert("", "end", values=(
                item["Code"],
                item["Name"],
                item["Current Stock"],
                item["Minimum Required"]
            ))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        def export_pdf():
            path = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
            )
            if not path:
                return
            ok = self.system.export_critical_stock_pdf(path)
            if ok:
                messagebox.showinfo("Success", f"PDF generated in:\n{path}")
            else:
                messagebox.showinfo(
                    "Info", "There're not critical stocks to generate a PDF."
                )

        ttk.Button(
            button_frame, text="Export PDF", command=export_pdf
        ).grid(row=0, column=0, padx=5)
        ttk.Button(
            button_frame, text="Close", command=dialog.destroy
        ).grid(row=0, column=1, padx=5)

def simple_input_dialog(prompt):
    dialog = tk.Toplevel()
    dialog.title("Input")
    dialog.resizable(False, False)
    dialog.grab_set()

    dialog.update_idletasks()
    width = 300
    height = 130
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")

    frame = ttk.Frame(dialog, padding=15)
    frame.pack(fill="both", expand=True)

    label = ttk.Label(frame, text=prompt)
    label.pack(padx=10, pady=(0, 10))
    entry = ttk.Entry(frame, width=30)
    entry.pack()
    entry.focus_set()

    def submit():
        dialog.result = entry.get()
        dialog.destroy()

    button = ttk.Button(frame, text="OK", command=submit)
    button.pack(pady=(10, 5))

    dialog.bind("<Return>", lambda event: submit())
    dialog.wait_window()
    return getattr(dialog, 'result', None)
