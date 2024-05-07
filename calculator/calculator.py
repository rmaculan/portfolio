from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont

class Calculator(QWidget): # Inherit from QWidget instead of QObject
    def __init__(self):
        super().__init__() # Call the parent class constructor
        self.app = QApplication([])
        self.main_window = QWidget()
        self.main_window.setWindowTitle('Calculator')
        self.main_window.resize(300, 300)
       
        print("Calculator is running")

        # Define text_box as an instance variable
        self.text_box = QLineEdit()
        self.grid = QGridLayout()

        self.bold_font = QFont()
        self.bold_font.setBold(True)
        self.bold_font.setPointSize(20)

        self.buttons = [
               "7", "8", "9", "/", 
               "4", "5", "6", "*", 
               "1", "2", "3", "-", 
               "0", ".", "=", "+"
               ]

        self.clear = QPushButton("C")
        self.delete = QPushButton("<")

        # for loop for buttons
        self.row = 0
        self.col = 0
        for text in self.buttons:
            button = QPushButton(text)
            button.clicked.connect(self.button_click) # Connect the signal to the slot
            button.setFont(self.bold_font)
            self.grid.addWidget(button, self.row, self.col)
            self.col += 1
            if self.col > 3:
                self.col = 0
                self.row += 1

        # Create a layout and add the text box and grid to it
        self.master_layout = QVBoxLayout()
        self.master_layout.addWidget(self.text_box)
        self.master_layout.addLayout(self.grid)

        self.button_row = QHBoxLayout()
        self.button_row.addWidget(self.clear)
        self.button_row.addWidget(self.delete)

        self.master_layout.addLayout(self.button_row)
        self.main_window.setLayout(self.master_layout)

        # Show the window after setting up the layout
        self.main_window.show()

    
    def button_click(self):
        button = self.sender() # Get the button that was clicked
        text = button.text() # Get the text of the clicked button
        if text == "=":
            symbol = self.text_box.text()
            try:
                self.res = eval(symbol)
                self.text_box.setText(str(self.res))
            except Exception as e:
                print("Error", e)
            return # Prevent further execution for "=" button
        elif text == "C":
            self.text_box.clear()
        elif text == "<":
            current_value = self.text_box.text()
            self.text_box.setText(current_value[:-1])
        else:
            current_value = self.text_box.text()
            new_value = current_value + text
            self.text_box.setText(new_value)

if __name__ == '__main__':
    app = QApplication([])
    calc = Calculator()
    app.exec_()
