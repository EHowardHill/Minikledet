import sys
import qdarktheme
from functools import partial
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QTextDocument, QIcon
from PySide6.QtWidgets import QVBoxLayout, QApplication, QMainWindow, QTextEdit, QPushButton

# Random new line

reference = {
    'C':'ק',
    'r':'ר',
    'a':'א',
    'e':'א',
    'T':'ט',
    'v':'ו',
    'u':'ו',
    'N':'ן',
    'M':'ם',
    'f':'פ',
    'S':'ש',
    'd':'ד',
    'g':'ג',
    'k':'כ',
    'A':'ע',
    'y':'י',
    'i':'י',
    'c':'ח',
    'l':'ל',
    'K':'ך',
    'F':'ף',
    'z':'ז',
    's':'ס',
    'b':'ב',
    'h':'ה',
    'n':'נ',
    'm':'מ',
    'x':'צ',
    't':'ת',
    'X':'ץ'
}

class HebrewKeyboard(QMainWindow):

    def __init__(self):

        import os

        # If you plan to use to pyinstaller
        icon_path = os.path.join(os.path.abspath(os.getcwd()), r'mini icon.png')

        super().__init__()
        self.setFixedSize(330, 330)
        self.setWindowTitle("Minikledet")
        self.setWindowIcon(QIcon(icon_path))
        self.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")

        # Create text input element
        self.text_input = QTextEdit(self)

        self.text_input.textChanged.connect(partial(self.on_text_change))
        self.text_input.setGeometry(5, 106, 320, 330 - 106 - 5 - 32)

        # Create buttons for Hebrew alphabet
        self.buttons = []

        letters = [
            ['ק','ר','א','ט','ו','ן','ם','פ'],
            ['ש','ד','ג','כ','ע','י','ח','ל','ך','ף'],
            ['ז','ס','ב','ה','נ','מ','צ','ת','ץ']
        ]

        x = 5
        y = 5
        for block in letters:
            for letter in block:
                button = QPushButton(letter, self)
                button.setGeometry(x,y,32,32)
                button.clicked.connect(partial(self.append_text, letter))
                for ref in reference.keys():
                    if reference[ref] == letter:
                        button.setToolTip(ref)
                        break
                x += 32
            x = 5
            y += 32

        # עותק
        button = QPushButton("Copy / העתק", self)
        button.clicked.connect(partial(self.copy_text))
        button.setGeometry(5,295,320,32)

        # Show window
        self.show()

    def append_text(self, letter):
        """Appends the letter to the text input element"""
        self.text_input.insertPlainText(letter)

    def copy_text(self, letter):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.text_input.toPlainText(), mode=cb.Clipboard)

    def on_text_change(self):
        self.text_input.textChanged.disconnect()
        self.text_input.textCursor().beginEditBlock()
        doc = self.text_input.document()
        for letter in reference.keys():
            while True:
                cursor = doc.find(letter, QTextCursor(doc), QTextDocument.FindCaseSensitively)
                if cursor.isNull():
                    break
                else:
                    cursor.insertText(reference[letter])
        self.text_input.textCursor().endEditBlock()
        self.text_input.textChanged.connect(partial(self.on_text_change))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.enable_hi_dpi()
    qdarktheme.setup_theme()
    keyboard = HebrewKeyboard()
    sys.exit(app.exec())