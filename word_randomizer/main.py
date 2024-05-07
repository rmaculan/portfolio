from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout,  QVBoxLayout, QWidget, QLabel, QPushButton

from random import choice

app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle('My Portfolio')
main_window.resize(300, 300)

#Create app opbjects
title=QLabel('My Portfolio')

text1=QLabel('?')
text2=QLabel('?')
text3=QLabel('?')

button1 = QPushButton('Add stock')
button2 = QPushButton('Remove stock')
button3 = QPushButton('Button 3') # Define button3 here

my_words = ['design', 'development', 'testing', 'deployment', 'maintenance', 'support']

main_layout = QVBoxLayout()

row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()

row1.addWidget(title, alignment=Qt.AlignHCenter)

row2.addWidget(text1, alignment=Qt.AlignHCenter)
row2.addWidget(text2, alignment=Qt.AlignHCenter)
row2.addWidget(text3, alignment=Qt.AlignHCenter)

row3.addWidget(button1)
row3.addWidget(button2)
row3.addWidget(button3)

main_layout.addLayout(row1)
main_layout.addLayout(row2)
main_layout.addLayout(row3)

main_window.setLayout(main_layout)

# app functions
def random_word():
    word = choice(my_words)
    text1.setText(word)

def random_word2():
    word = choice(my_words)
    text2.setText(word)

def random_word3():
    word = choice(my_words)
    text3.setText(word)

# app events
    
button1.clicked.connect(random_word)
button2.clicked.connect(random_word2)
button3.clicked.connect(random_word3)


main_window.show()
app.exec_()




