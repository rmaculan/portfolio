# Import Modules for expense tracker app
from PyQt5.QtWidgets import QApplication, QDateEdit, QComboBox, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate
import sys

# App Class
class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
    # Main App Objects $ Settings

        # Set Window Title
        self.setWindowTitle("Expense Tracker")

        # Set Date
        self.date_box = QDateEdit()

        # Create Dropdown
        self.dropdown = QComboBox()

        # Set Amount
        self.amount = QLineEdit()

        # Create Description
        self.description = QLineEdit()

        # Set Window Size
        self.setFixedSize(800, 600)

        # Set Main Layout
        self.layout = QVBoxLayout()

        # Set Central Widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Create Widgets
        self.title = QLabel("Expense Tracker")
        self.layout.addWidget(self.title)

        # Create Table
        self.table = QTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(5) # Id, Date, Category, Amount, Description
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Amount", "Description"])

        self.dropdown.addItems(["Food", "Transport", "Entertainment", "Utilities", "Rent", "Other"])

        # Customize Table Appearance
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # Make columns stretch to fill the table
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) # Make rows stretch to fill the table
        self.table.setShowGrid(False) # Hide grid lines

        # Create Buttons
        # Create Buttons
        self.add_expense_button = QPushButton("Add Expense")
        self.delete_expense_button = QPushButton("Delete Expense")
        self.layout.addWidget(self.add_expense_button)

        # Add and Delete Expense Button Functionality
        self.add_expense_button.clicked.connect(self.add_expense)
        self.delete_expense_button.clicked.connect(self.delete_expense)

        # Design App with Layouts
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        # Add Widgets to Layout
        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)
        #
        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description)
        #
        self.row3.addWidget(self.add_expense_button)
        self.row3.addWidget(self.delete_expense_button)

        self.layout.addLayout(self.row1)
        self.layout.addLayout(self.row2)
        self.layout.addLayout(self.row3) # Use addLayout for QHBoxLayouts
        self.layout.addWidget(self.table)
        
        # Set Layout
    # Load Table Function
    def load_table(self):
        self.table.setRowCount(0)
        query = QSqlQuery()
        if not query.exec("SELECT * FROM expenses"):
            QMessageBox.critical(self, "Error", "Failed to load expenses: {}".format(query.lastError().text()))
            return
        while query.next():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(query.value(0))))
            self.table.setItem(row, 1, QTableWidgetItem(query.value(1)))
            self.table.setItem(row, 2, QTableWidgetItem(query.value(2)))
            self.table.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
            self.table.setItem(row, 4, QTableWidgetItem(query.value(4)))

            row += 1

    # Calculate total expenses
    def calculate_total(self):
        query = QSqlQuery()
        if not query.exec("SELECT SUM(amount) FROM expenses"):
            QMessageBox.critical(self, "Error", "Failed to calculate total expenses: {}".format(query.lastError().text()))
            return
        query.next()
        total = query.value(0)
        return total

    # Add Expense Function
    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        query = QSqlQuery()
        query.prepare("""
                      INSERT INTO expenses (date, category, amount, description) 
                      VALUES (?, ?, ?, ?)
                      """)
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        if not query.exec():
            QMessageBox.critical(self, "Error", "Failed to add expense: {}".format(query.lastError().text()))
        else:
            self.load_table()
            self.display_total_expenses()

        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()
        self.display_total_expenses()
        

    # Delete Expense Function
    def delete_expense(self):
        row = self.table.currentRow()
        if row < 0:
            return
        expense_id = int(self.table.item(row, 0).text())

        confirmation = QMessageBox.question(self, "Delete Expense", "Are you sure you want to delete this expense?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)
        if not query.exec():
            QMessageBox.critical(self, "Error", "Failed to delete expense: {}".format(query.lastError().text()))
        else:
            self.load_table()

        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()
        self.display_total_expenses()

    def display_total_expenses(self):
        total = self.calculate_total()
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem("Total"))
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setItem(row, 2, QTableWidgetItem(""))
        self.table.setItem(row, 3, QTableWidgetItem(str(total)))
        self.table.setItem(row, 4, QTableWidgetItem(""))

# Create Database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expenses.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Database Connection Error: {}".format(database.lastError().text()))
    sys.exit(1)

query = QSqlQuery()
query.exec(
    """
    CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT NOT NULL
    )
    """)


# Run App
if __name__ == "__main__":
    app = QApplication([])
    window = ExpenseTracker()
    window.show()
    app.exec_()
