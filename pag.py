from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QListWidget
from PyQt6.QtCore import Qt
from interfaz import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.user = "123"
        self.password = "123"
        self.buttonlogin.clicked.connect(self.iniciar_sesion)
        self.lbl_message = self.findChild(QLabel, "lbl_message")
        self.txt_user = self.findChild(QTextEdit, "txt_user")
        self.txt_pass = self.findChild(QTextEdit, "txt_pass")
        self.listWidget_menu = self.findChild(QListWidget, "listWidget_menu")
        self.listWidget_carrito = self.findChild(QListWidget, "listWidget_carrito")

        # Oculta elementos al inicio
        self.labelmenumsg.setVisible(False)
        self.label.setVisible(True)
        self.label_2.setVisible(True)
        self.label_3.setVisible(True)
        self.txt_user.setVisible(True)
        self.txt_pass.setVisible(True)
        self.buttonlogin.setVisible(True)
        #capuchino
        self.capimg.setVisible(False)
        self.listWidget.setVisible(False)
        self.capmenos.setVisible(False)
        self.capmas.setVisible(False)
        #expreso
        self.expresoimg.setVisible(False)
        self.exmas.setVisible(False)
        self.exmenos.setVisible(False)
        #frappe
        self.frapimg.setVisible(False)
        self.frapmas.setVisible(False)
        self.frapmenos.setVisible(False)
        #chocolate
        self.chocimg.setVisible(False)
        self.chocomas.setVisible(False)
        self.chocmenos.setVisible(False)

 

    def iniciar_sesion(self):
        if self.user == self.txt_user.toPlainText() and self.password == self.txt_pass.toPlainText():
            # Muestra elementos después del inicio de sesión exitoso
            self.labelmenumsg.setVisible(True)
            self.label.setVisible(False)
            self.label_2.setVisible(False)
            self.label_3.setVisible(False)
            self.txt_user.setVisible(False)
            self.txt_pass.setVisible(False)
            self.buttonlogin.setVisible(False)
            self.listWidget.setVisible(False)
            self.lbl_message.setVisible(False)
            #capuchino
            self.capmenos.setVisible(True)
            self.capmas.setVisible(True)
            self.capimg.setVisible(True)
            #expreso
            self.expresoimg.setVisible(True)
            self.exmas.setVisible(True)
            self.exmenos.setVisible(True)
            #frappe
            self.frapimg.setVisible(True)
            self.frapmas.setVisible(True)
            self.frapmenos.setVisible(True)
            #chocolate
            self.chocimg.setVisible(True)
            self.chocomas.setVisible(True)
            self.chocmenos.setVisible(True)
 

            
        else:
            self.lbl_message.setText("Denegado")

    def agregar_al_carrito(self):
        # Implementa la lógica para agregar elementos al carrito
        pass

    def quitar_del_carrito(self):
        # Implementa la lógica para quitar elementos del carrito
        pass

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
