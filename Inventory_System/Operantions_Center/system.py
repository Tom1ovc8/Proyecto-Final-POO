from Inventory_System.Inventory_Management.inventory import Inventory
from Inventory_System.Inventory_Management.inventory_record import InventoryRecord
from Inventory_System.Inventory_Management.location import Location
from Inventory_System.Inventory_Management.stock import Stock
from Inventory_System.Transactions.movements import Movement
from Inventory_System.Transactions.bills import Bill
from Inventory_System.Operantions_Center.extracts import Extracts
from Inventory_System.Operantions_Center.generatepdf import (
    ActorHistoryPDF, BillPDF, CriticalStockPDF,
    InventoryReportPDF, MovementsReportPDF, SalesSummaryPDF
)   

class System(Inventory):
    def __init__(self):
        super().__init__()
        self.bills = {}
        self.customers = {}
        self.suppliers = {}

    def entry_record(self, product, amount, supplier, reason):
        code = product._code
        if code in self.records:
            raise ValueError(f"Product code {code} is already in inventory.")
        
        location = Location.assign_location(product.category, product._code)
        stock = Stock(0, 20, 200)
        record = InventoryRecord(product, stock, location)
        self.add_record(record)
        movement = Movement(product, amount, supplier, reason)
        self.add_movement(movement)
        print(f"Product {product.name} added at {location.to_dict()}")

    def make_sale(self, product_code, amount, customer, reason):
        if product_code not in self.records:
            raise ValueError("Product code not found in inventory.")
        
        record = self.records[product_code]
        movement = Movement(record.product, amount, customer, reason)
        delta = movement.get_delta()
        stock = record.stock

        if not stock.is_valid_update(delta):
            print(
                f"Movement for {record.product.name} failed due "
                  "to insufficient stock."
            )
            return False

        self.add_movement(movement) 
        print(f"Movement for {record.product.name} recorded successfully.")
        return True
    
    def add_customer(self, customer):
        if customer._id in self.customers:
            print(f"Customer '{customer.name}' already exists.")
        else:
            self.customers[customer._id] = customer
            print(f"Customer '{customer.name}' added.")

    def add_supplier(self, supplier):
        if supplier._id in self.suppliers:
            print(f"Supplier '{supplier.name}' already exists.")
        else:
            self.suppliers[supplier._id] = supplier
            print(f"Supplier '{supplier.name}' added.")

    def generate_customer_history(self, customer_id):
        if customer_id not in self.customers:
            raise ValueError(f"Customer not found")
        return [
            movement.to_dict() for movement in self.movements
                if (
                    movement._actor_id == customer_id and 
                    movement.actor_type == "customer"
                )
        ]
        
    def generate_supplier_history(self, supplier_id):
        if supplier_id not in self.suppliers:
            raise ValueError(f"Supplier not found")
        return [
            movement.to_dict() for movement in self.movements
                if (movement._actor_id == supplier_id 
                    and movement.actor_type == "supplier"
                )
        ]
    
    def create_bill(self, entity, movements, payment_method):
        bill = Bill(entity, payment_method)

        for movement in movements:
            if movement.actor._id != entity._id:
                raise ValueError("Movement does not belong to this entity.")

            sale_price = movement.final_price
            bill.add_item(
                movement.product,
                movement.amount,
                sale_price
            )
            movement._bill_id = bill._bill_id

        self.bills[bill._bill_id] = bill

        total = bill.calculate_total()
        if not payment_method.pay(total):
            print("Payment failed.")
            return None

        print(f"Bill {bill._bill_id} created for {entity.name}.")
        return bill

    def export_full_system(self, path="full_backup.json"):
        Extracts.export_full_system(self, path)

    def load_full_backup(self, path="full_backup.json"):
        Extracts.load_full_backup(path, self)

    def export_inventory_pdf(self, filename="inventory_report.pdf"):
        data = [r.to_dict() for r in self.records.values()]
        pdf = InventoryReportPDF()
        pdf.generate(data)
        pdf.output(filename)

    def export_movements_pdf(self, filename="movements_report.pdf"):
        data = [m.to_dict() for m in self.movements]
        pdf = MovementsReportPDF()
        pdf.generate(data)
        pdf.output(filename)

    def export_bill_pdf(self, bill_id: str, filename="bill_report.pdf"):
        try:
            bill = self.bills.get(bill_id)
            if not bill:
                raise ValueError(f"Bill ID {bill_id} not found.")
            
            if not filename.lower().endswith(".pdf"):
                filename += ".pdf"

            pdf = BillPDF()
            pdf.generate(bill, filename)
            print(f"Bill exported: {filename}")

        except Exception as e:
            print(f"Error generating PDF Bill: {e}")

    def export_critical_stock_pdf(self, filename="critical_stock.pdf"):
        critical = super().get_critical_records()
        if not critical:
            print("No hay stocks críticos.")
            return False
        pdf = CriticalStockPDF()
        pdf.generate(critical, filename)
        return True

    def export_actor_history_pdf(self, actor_id: str, filename=None):
        try:
            actor = (
                self.customers.get(actor_id) or 
                self.suppliers.get(actor_id)
            )
            if not actor:
                raise ValueError(f"No actor found with ID {actor_id}")

            actor_type = (
                "customer" if actor_id in self.customers else "supplier"
            )
            actor_name = actor.name

            filtered_movements = [
                m for m in self.movements if m._actor_id == actor_id
            ]

            if not filtered_movements:
                print(f"No movements found for {actor_type} '{actor_name}'.")
                return

            if not filename:
                filename = (
                    f"{actor_type}_{actor_name.replace(' ', '_')}_history.pdf"
                )

            pdf = ActorHistoryPDF(actor_name, actor_type)
            pdf.generate(filtered_movements, filename)
            print(f"History PDF generated: {filename}")

        except Exception as e:
            print(f"Error generating actor history PDF: {e}")

    def export_sales_summary_pdf(
        self, filename="sales_summary.pdf", product_code=None
    ):
        try:
            movements = self.movements
            if product_code:
                movements = [
                    m for m in movements if m.product._code == product_code
                ]

            if not movements:
                print("There're no data to make a report.")
                return

            summary = {}
            for m in movements:
                code = m.product._code
                if code not in summary:
                    summary[code] = {
                        "name": m.product.name,
                        "in": {"qty": 0, "cost": 0.0},
                        "out": {"qty": 0, "cost": 0.0}
                    }

                if m.type == "in":  # Compras
                    summary[code]["in"]["qty"] += m.amount
                    summary[code]["in"]["cost"] += m.amount * m.product._price
                else:  # Salidas (ventas)
                    summary[code]["out"]["qty"] += m.amount
                    summary[code]["out"]["cost"] += m.amount * m.final_price

            title = f"Resumen de Ventas y Compras"
            if product_code:
                title += (
                    f" - Producto: {summary[product_code]['name']} "
                    f"({product_code})"
                )

            pdf = SalesSummaryPDF(title)
            pdf.generate(summary, filename)
            print(f"Resumen generado en: {filename}")

        except Exception as e:
            print(f"Error generando el resumen: {e}")
