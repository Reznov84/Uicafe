from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from interfaz import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.user = "usuario"
        self.password = "contrasena"
        self.buttonlogin.clicked.connect(self.iniciar_sesion)
        self.lbl_message = self.findChild(QLabel, "lbl_message")

    def iniciar_sesion(self):
        if self.user == self.txt_user.toPlainText() and self.password == self.txt_pass.toPlainText():
            self.lbl_message.setText("Bienvenido")
        else:
            self.lbl_message.setText("Denegado")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
