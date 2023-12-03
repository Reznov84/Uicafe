from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from interfaz import Ui_MainWindow
import csv
from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance as Message  # Importa la clase Message

account_sid = 'ACf11a2cbae1c24695c1bcfcec6c4a2ccd'
auth_token = 'ad3232328ad7b826a90afa1ca5ae2ade'
client = Client(account_sid, auth_token)


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

        #precio de las bebidas
        self.precios = {}

        #cargar menu desde csv
        self.cargar_menu_desde_csv('menu.csv')

        #ocultar elementos antes de iniciar sesion
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

        #rastrear la cantidad y el precio total de cada bebida en el carrito
        self.carrito = {}

        #conecta el boton "BuyButton" para agregar la compra al carrito y guardar en CSV
        self.BuyButton.clicked.connect(self.agregar_al_carrito)

        #conecta la señal itemClicked del listWidget_menu a la funcion agregar_bebida_al_carrito
        self.listWidget_menu.itemClicked.connect(self.agregar_bebida_al_carrito)

    def cargar_menu_desde_csv(self, archivo_csv):
        #limpiar el menu 
        self.listWidget_menu.clear()
        self.precios.clear()

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
            #muestra los elementos al iniciar sesion
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
        #aumentar cantidad de bebida
        if bebida in self.carrito:
            self.carrito[bebida]['cantidad'] += cantidad
        else:
            #añadir bebida por primera vez
            self.carrito[bebida] = {'cantidad': cantidad}

        cantidad_actual = self.carrito[bebida]['cantidad']

        #si no hay bebida, desabilitar restar
        if cantidad_actual == 0:
            self.eliminar_item_carrito(bebida)
        else:
            #actualiza la lista del carrito
            self.actualizar_lista_carrito(bebida, cantidad_actual)

        #mostrar total
        self.actualizar_total_compra()

    def actualizar_lista_carrito(self, bebida, cantidad_actual):
        #busca si la bebida ya esta en el carrito
        for index in range(self.listWidget_carrito.count()):
            item = self.listWidget_carrito.item(index)
            widget = self.listWidget_carrito.itemWidget(item)
            if widget and widget.bebida == bebida:
                #actualiza la cantidad en el carrito
                widget.label.setText(
                    f"{bebida} - Cantidad: {cantidad_actual} - Precio Unitario: ${self.precios[bebida]:.2f} - Total: ${cantidad_actual * self.precios[bebida]:.2f}")
                return

        #si la bebida no esta en el carrito, agrega un nuevo elemento
        widget = BeverageWidget(bebida, cantidad_actual, self.precios[bebida])
        widget.quitar_button.clicked.connect(lambda _, b=bebida: self.quitar_del_carrito(b))
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.listWidget_carrito.addItem(item)
        self.listWidget_carrito.setItemWidget(item, widget)

    def eliminar_item_carrito(self, bebida):
        #elimina la bebida del carrito y actualiza el diccionario
        del self.carrito[bebida]
        self.listWidget_carrito.clear()
        for key, value in self.carrito.items():
            if value['cantidad'] > 0:
                self.actualizar_lista_carrito(key, value['cantidad'])

    def actualizar_total_compra(self):
        #mostrar total 
        total = sum(item['cantidad'] * self.precios[bebida] for bebida, item in self.carrito.items())
        self.labelmenumsg.setText(f"Total de la compra: ${total:.2f}")

    def guardar_en_csv(self):
        #abrir archivo csv
        with open('ventas.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            #escribir las compras
            for bebida, item in self.carrito.items():
                cantidad = item['cantidad']
                precio_unitario = self.precios.get(bebida, 0.0)
                precio_total = cantidad * precio_unitario

                #verificar que se haya hecho una compra
                if cantidad > 0:
                    writer.writerow([bebida, cantidad, precio_unitario, precio_total])


    def enviar_mensaje_twilio(self, cuerpo_mensaje):
        try:
            mensaje = client.messages.create(
                body=cuerpo_mensaje,
                from_='+12675206550',  
                to='+522225635184'
            )

            print(f'Mensaje de confirmación enviado con SID: {mensaje.sid}')

        except Exception as e:
            print(f'Error al enviar el mensaje: {e}')


    def agregar_al_carrito(self):
        #verifica inventario
        if not self.verificar_inventario():
            #mensaje de error de inventario
            print("No hay suficiente inventario para realizar la compra.")
            return

        #guardar en csv
        self.guardar_en_csv()

        #limpia el carrito despues de la compra
        self.listWidget_carrito.clear()
        self.actualizar_total_compra()

        #actualiza inventario
        self.actualizar_inventario()

        #mensaje de texto
        cuerpo_mensaje = f"Compra realizada. Total: ${self.labelmenumsg.text().split(': $')[1]}"
        self.enviar_mensaje_twilio(cuerpo_mensaje)

    def agregar_bebida_al_carrito(self, item):
        #texto para el carrito
        bebida_texto = item.text()

        #nombre de la bebida
        bebida = bebida_texto.split(":")[0].strip().lower()

        #bebida y cantidad de 1
        self.actualizar_carrito(bebida, 1)

    def quitar_del_carrito(self, bebida):
        #disminuir cantidaden 1
        self.actualizar_carrito(bebida, -1)

    def verificar_inventario(self):
        #verifica la cantidad en el inventario
        for bebida, item in self.carrito.items():
            cantidad = item['cantidad']
            requisitos = self.obtener_requisitos(bebida)

            #comprueba por ingradiente
            for ingrediente, cantidad_requerida in requisitos.items():
                if self.obtener_cantidad_inventario(ingrediente) < cantidad * cantidad_requerida:
                    #mensaje de error en el labelmenumsg
                    self.labelmenumsg.setText(f"No hay suficiente inventario para {bebida}.")
                    return False  

        #hay suficiente insumo
        self.labelmenumsg.setText("Inventario verificado: Suficiente inventario.")
        return True

    def obtener_requisitos(self, bebida):
        #leer los requisitos de la bebida
        try:
            with open('menu.csv', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Bebida'].lower() == bebida:
                        return {ingrediente: int(cantidad) for ingrediente, cantidad in row.items() if
                                ingrediente.lower() != 'precio' and ingrediente.lower() != 'bebida'}
        except FileNotFoundError:
            print("Archivo CSV 'menu.csv' no encontrado.")
        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")

        return {}

    def obtener_cantidad_inventario(self, ingrediente):
        #obtiene la cantidad actual en inventario para un ingrediente especifico
        try:
            with open('inventario.csv', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Ingrediente'].lower() == ingrediente.lower():
                        return int(row['Cantidad'])
        except FileNotFoundError:
            print("Archivo CSV 'inventario.csv' no encontrado.")
        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")

        return 0

    def actualizar_inventario(self):
        #actualiza despues de la compra
        for bebida, item in self.carrito.items():
            cantidad = item['cantidad']
            requisitos = self.obtener_requisitos(bebida)

            #resta del inventario
            for ingrediente, cantidad_requerida in requisitos.items():
                cantidad_actual = self.obtener_cantidad_inventario(ingrediente)
                nueva_cantidad = cantidad_actual - cantidad * cantidad_requerida
                self.actualizar_cantidad_inventario(ingrediente, nueva_cantidad)

    def actualizar_cantidad_inventario(self, ingrediente, nueva_cantidad):
        try:
            with open('inventario.csv', 'r', newline='') as file:
                lines = file.readlines()

            with open('inventario.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Ingrediente', 'Cantidad'])

                for line in lines[1:]:  
                    row = line.strip().split(',')
                    if row[0].lower() == ingrediente.lower():
                        writer.writerow([ingrediente, nueva_cantidad])
                    else:
                        writer.writerow(row)
        except FileNotFoundError:
            print("Archivo CSV 'inventario.csv' no encontrado.")
        except Exception as e:
            print(f"Error al escribir en el archivo CSV: {e}")

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
