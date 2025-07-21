from datetime import datetime

from fpdf import FPDF

from Inventory_System.Transactions.payment import Cash


class PDF(FPDF):
    def __init__(self, title="Report"):
        super().__init__()
        self.title = title

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, self.title, ln=True, align="C")
        self.set_font("Helvetica", "", 10)
        self.cell(
            0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}",
            ln=True, align="C"
        )
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def setup_page(self):
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()

    def _add_table_header(self, headers, col_widths):
        self.set_font("Helvetica", "B", 10)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, align="C")
        self.ln()

    def _add_table_row(self, row_data, col_widths, line_height=8):
        self.set_font("Helvetica", "", 10)
        for i, cell in enumerate(row_data):
            self.cell(col_widths[i], line_height, str(cell), border=1)
        self.ln()

    def generate_table(self, headers, rows, col_widths):
        self._add_table_header(headers, col_widths)
        for row in rows:
            self._add_table_row(row, col_widths)


class InventoryReportPDF(PDF):
    def __init__(self):
        super().__init__(title="Inventory Report")

    def generate(self, records, filename="inventory_report.pdf"):
        self.setup_page()
        headers = [
            "Code", "Name", "Category", "Stock",
            "Min", "Max", "Location", "State"
            ]
        col_widths = [15, 30, 25, 15, 15, 15, 35, 40]
        rows = []

        for record in records:
            product = record["product"]
            stock = record["stock"]
            location = record["location"]

            state_data = product["state"]
            if "expiration_date" in state_data:
                exp = state_data["expiration_date"]
                state_str = f"Expires: {exp[0]:04d}-{exp[1]:02d}-{exp[2]:02d}"
            elif "condition" in state_data:
                state_str = f"Condition: {state_data['condition']}"
            else:
                state_str = "Unknown"

            rows.append([
                product["code"],
                product["name"],
                product["category"],
                stock["actual_stock"],
                stock["minimum_stock"],
                stock["maximum_stock"],
                f"Aisle {location['aisle']} - Shelf {location['shelf']}",
                state_str
            ])

        self.generate_table(headers, rows, col_widths)
        self.output(filename)

class MovementsReportPDF(PDF):
    def __init__(self):
        super().__init__(title="Inventory Movements Report")

    def generate(self, movements, filename="movements_report.pdf"):
        self.setup_page()
        headers = [
            "Date", "Type", "Product Code", 
            "Quantity", "Actor", "Reason"
            ]
        col_widths = [25, 10, 25, 20, 60, 50]
        rows = []

        for movement in movements:
            rows.append([
                movement["Date"],
                movement["Type"],
                movement["Code"],
                movement["Quantity"],
                movement["Actor"],
                movement["Reason"]
            ])

        self.generate_table(headers, rows, col_widths)
        self.output(filename)

class BillPDF(PDF):
    def generate(self, bill, filename="bill_report.pdf"):
        self.add_page()
        self.set_font("Helvetica", "", 12)

        self.cell(0, 10, f"Bill ID: {bill._bill_id}", ln=True)
        self.cell(0, 10, f"Date: {bill.date.strftime('%Y-%m-%d')}", ln=True)
        self.cell(0, 10, f"Entity: {bill.entity.name}", ln=True)
        self.cell(0, 10, f"Type: {bill.entity_type}", ln=True)
        self.cell(0, 10, f"Payment Method: {bill.payment_method}", ln=True)
        if isinstance(bill.payment_method, Cash):
            total = bill.calculate_total()
            given = bill.payment_method.cash_given
            if given >= total:
                change = given - total
                self.cell(
                    0, 10, f"Paid for: ${given:.2f} - Change: ${change:.2f}",
                    ln=True
                )
            else:
                lack = total - given
                self.cell(
                    0, 10, f"Cash Insuficient. Lack: ${lack:.2f}", ln=True
                )
        self.ln(5)

        self.set_font("Helvetica", "B", 10)
        headers = ["Code", "Product", "Amount", "Unit Cost", "Subtotal"]
        col_widths = [30, 50, 30, 30, 30]
        self._add_table_header(headers, col_widths)

        self.set_font("Helvetica", "", 10)
        for item in bill.items:
            self._add_table_row([
                item.product._code,
                item.product.name,
                item.quantity,
                f"${item.price:.2f}",
                f"${item.quantity * item.price:.2f}"
            ], col_widths)

        self.set_font("Helvetica", "B", 11)
        self.cell(sum(col_widths[:-1]), 10, "Total", border=1, align="R")
        self.cell(
            col_widths[-1], 10, f"${bill.calculate_total():.2f}",
            border=1, align="R"
        )
        self.ln()
        self.output(filename)

class CriticalStockPDF(PDF):
    def __init__(self):
        super().__init__(title="Critic Stock")

    def generate(self, records: list, filename="critical_stock.pdf"):
        self.add_page()

        headers = [
            "Code", "Product", "Category", "Stock", "Minimum", "Location"
        ]
        col_widths = [20, 45, 30, 20, 25, 50]

        rows = []
        for record in records:
            product = record.product
            stock = record.stock
            location = record.location

            rows.append([
                product._code,
                product.name,
                product.category,
                stock.get_actual_stock(),
                stock.minimum_stock,
                f"Aisle {location.aisle} - Shelf {location.shelf}"
                ])
            
        self.generate_table(headers, rows, col_widths)
        self.output(filename)

class ActorHistoryPDF(PDF):
    def __init__(self, actor_name, actor_type):
        title = f"History for {actor_type.capitalize()}: {actor_name}"
        super().__init__(title)

    def generate(self, movements: list, filename="actor_history.pdf"):
        self.setup_page()

        headers = ["Date", "Product", "Code", "Amount", "Type", "Reason"]
        col_widths = [25, 45, 25, 15, 20, 60]

        rows = []
        for movement in movements:
            rows.append([
                movement.date.strftime("%Y-%m-%d"),
                movement.product.name,
                movement.product._code,
                movement.amount,
                movement.type,
                movement.reason
            ])

        self.generate_table(headers, rows, col_widths)
        self.output(filename)

class SalesSummaryPDF(PDF):
    def __init__(self, title="Sales Summary Report"):
        super().__init__(title)

    def generate(self, summary_data: dict, filename="sales_summary.pdf"):
        self.setup_page()

        headers = [
            "Code", "Product", "IN Qty", "IN Cost", "OUT Qty", "OUT Sales"
        ]
        col_widths = [30, 50, 25, 30, 25, 30]

        rows = []
        for code, data in summary_data.items():
            rows.append([
                code,
                data["name"],
                str(data["in"]["qty"]),
                f"${data['in']['cost']:.2f}",
                str(data["out"]["qty"]),
                f"${data['out']['cost']:.2f}"
            ])

        self.generate_table(headers, rows, col_widths)
        self.output(filename)
        
        
