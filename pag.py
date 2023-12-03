from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from interfaz import Ui_MainWindow
import csv

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

        # Precios de las bebidas
        self.precios = {}

        # Cargar el menú desde un archivo CSV
        self.cargar_menu_desde_csv('menu.csv')

        # Oculta elementos al inicio
        self.listWidget_menu.setVisible(False)
        self.BuyButton.setVisible(False)
        self.listWidget_carrito.setVisible(False)
        self.labelmenumsg.setVisible(False)
        self.label.setVisible(True)
        self.label_2.setVisible(True)
        self.label_3.setVisible(True)
        self.txt_user.setVisible(True)
        self.txt_pass.setVisible(True)
        self.buttonlogin.setVisible(True)

        # Diccionario para rastrear la cantidad y el precio total de cada bebida en el carrito
        self.carrito = {'capuchino': {'cantidad': 0, 'precio_total': 0.0},
                        'expreso': {'cantidad': 0, 'precio_total': 0.0},
                        'frappe': {'cantidad': 0, 'precio_total': 0.0},
                        'chocolate': {'cantidad': 0, 'precio_total': 0.0}}

        # Conecta el botón "BuyButton" para agregar la compra al carrito y guardar en CSV
        self.BuyButton.clicked.connect(self.agregar_al_carrito)

        # Conecta la señal itemClicked del listWidget_menu a la función agregar_bebida_al_carrito
        self.listWidget_menu.itemClicked.connect(self.agregar_bebida_al_carrito)

    def cargar_menu_desde_csv(self, archivo_csv):
        try:
            with open(archivo_csv, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    bebida = row['Bebida']
                    precio = float(row['Precio'])
                    self.precios[bebida.lower()] = precio
                    item = QListWidgetItem(f"{bebida}: ${precio:.2f}")
                    self.listWidget_menu.addItem(item)
        except FileNotFoundError:
            print(f"Archivo CSV '{archivo_csv}' no encontrado.")
        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")

    def iniciar_sesion(self):
        if self.user == self.txt_user.toPlainText() and self.password == self.txt_pass.toPlainText():
            # Muestra elementos después del inicio de sesión exitoso
            self.listWidget_menu.setVisible(True)
            self.BuyButton.setVisible(True)
            self.listWidget_carrito.setVisible(True)
            self.labelmenumsg.setVisible(True)
            self.label.setVisible(False)
            self.label_2.setVisible(False)
            self.label_3.setVisible(False)
            self.txt_user.setVisible(False)
            self.txt_pass.setVisible(False)
            self.buttonlogin.setVisible(False)
            self.lbl_message.setVisible(False)
        else:
            self.lbl_message.setText("Denegado")

    def actualizar_carrito(self, bebida, cantidad):
        # Asegúrate de que la bebida esté en el carrito antes de intentar actualizar la cantidad
        if bebida in self.carrito:
            self.carrito[bebida]['cantidad'] += cantidad
            cantidad_actual = self.carrito[bebida]['cantidad']

            # Si la cantidad es 0, elimina el elemento del carrito y deshabilita el botón "-"
            if cantidad_actual == 0:
                self.eliminar_item_carrito(bebida)
            else:
                # Actualiza la lista del carrito
                self.actualizar_lista_carrito(bebida, cantidad_actual)

            # Calcula y muestra el total de la compra
            self.actualizar_total_compra()

    def actualizar_lista_carrito(self, bebida, cantidad_actual):
        # Busca si la bebida ya está en el carrito
        for index in range(self.listWidget_carrito.count()):
            item = self.listWidget_carrito.item(index)
            widget = self.listWidget_carrito.itemWidget(item)
            if widget and widget.bebida == bebida:
                # Actualiza la cantidad en el carrito
                widget.label.setText(
                    f"{bebida} - Cantidad: {cantidad_actual} - Precio Unitario: ${self.precios[bebida]:.2f} - Total: ${cantidad_actual * self.precios[bebida]:.2f}")
                return

        # Si la bebida no está en el carrito, agrega un nuevo elemento
        widget = BeverageWidget(bebida, cantidad_actual, self.precios[bebida])
        widget.quitar_button.clicked.connect(lambda _, b=bebida: self.quitar_del_carrito(b))
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.listWidget_carrito.addItem(item)
        self.listWidget_carrito.setItemWidget(item, widget)

    def eliminar_item_carrito(self, bebida):
        # Elimina la bebida del carrito y actualiza el diccionario
        self.listWidget_carrito.clear()
        for key, value in self.carrito.items():
            if value['cantidad'] > 0:
                self.actualizar_lista_carrito(key, value['cantidad'])

    def actualizar_total_compra(self):
        # Calcula y muestra el total de la compra
        total = sum(item['cantidad'] * self.precios[bebida] for bebida, item in self.carrito.items())
        self.labelmenumsg.setText(f"Total de la compra: ${total:.2f}")

    def guardar_en_csv(self):
        # Abre el archivo CSV en modo de escritura
        with open('ventas.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            # Escribe una fila con la información de la compra
            for bebida, item in self.carrito.items():
                cantidad = item['cantidad']
                precio_unitario = self.precios[bebida]
                precio_total = cantidad * precio_unitario

                # Si la cantidad es mayor que 0, guarda la compra en el archivo
                if cantidad > 0:
                    writer.writerow([bebida, cantidad, precio_unitario, precio_total])

    def agregar_al_carrito(self):
        # Agrega la compra al carrito y guarda en CSV
        self.guardar_en_csv()

    def agregar_bebida_al_carrito(self, item):
        # Obtiene el texto del elemento seleccionado en listWidget_menu
        bebida_texto = item.text()

        # Extrae el nombre de la bebida del texto
        bebida = bebida_texto.split(":")[0].strip().lower()

        # Añade la bebida al carrito con una cantidad de 1
        self.actualizar_carrito(bebida, 1)

    def quitar_del_carrito(self, bebida):
        # Disminuye la cantidad en el carrito y actualiza la lista del carrito
        self.actualizar_carrito(bebida, -1)

class BeverageWidget(QWidget):
    def __init__(self, bebida, cantidad, precio_unitario, *args, **kwargs):
        super(BeverageWidget, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()

        self.label = QLabel(
            f"{bebida} - Cantidad: {cantidad} - Precio Unitario: ${precio_unitario:.2f} - Total: ${cantidad * precio_unitario:.2f}")
        self.quitar_button = QPushButton("Quitar")

        layout.addWidget(self.label)
        layout.addWidget(self.quitar_button)

        self.bebida = bebida

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
