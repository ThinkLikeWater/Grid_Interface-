import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QPushButton, QMessageBox, QWidget, QGridLayout


class TabbedInterface(QMainWindow):
    def __init__(self, xml_file):
        super().__init__()

        self.setWindowTitle("Grid Interface and Message Box")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.load_from_xml(xml_file)

    def load_from_xml(self, xml_file="none"):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for tab_element in root.findall('tab'):
                tab_name = tab_element.get('name')
                tab = QWidget()
                self.tabs.addTab(tab, tab_name)

                grid_layout = QGridLayout()
                tab.setLayout(grid_layout)

                row, col = 0, 0
                for button_element in tab_element.findall('button'):
                    button_name = button_element.text.strip()
                    button = QPushButton(button_name)
                    button.clicked.connect(lambda _, name=button_name: self.show_message_box(name))
                    grid_layout.addWidget(button, row, col)
                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1

        except Exception as e:
            print(f"Error loading from XML: {str(e)}")

    @staticmethod
    def show_message_box(button_name):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Message")
        msg_box.setText(f"You pressed button '{button_name}'")
        msg_box.exec_()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        xml_file = "default.xml"
    else:
        xml_file = sys.argv[1]

    app = QApplication(sys.argv)
    window = TabbedInterface(xml_file)
    window.show()
    sys.exit(app.exec_())
