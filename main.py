import psycopg2
from psycopg2 import OperationalError
import customtkinter
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, CTkScrollableFrame
from CTkTable import CTkTable
import os
import glob
from PIL import Image, ImageTk
from datetime import date, datetime

customtkinter.set_default_color_theme("blue")

# Ventana principal de la aplicación, donde se encontrarán los almacenes registrados y se podrán crear nuevos almacenes y acceder a los ya existentes
class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.delete_button = None
        self.edit_button = None
        self.connect_button = None
        self.title("HERRAMIENTA DE ADMINISTRACIÓN DE INVENTARIO")
        self.geometry(f"{900}x{400}")
        self.resizable(False, False) 

        # Centar ventana
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 400) // 2
        self.geometry(f"+{x}+{y}")

        # Crear ventana popup de bienvenida
        def welcome_window():
            welcome_window = customtkinter.CTkToplevel()
            welcome_window.title("BIENVENIDO")
            welcome_window.geometry("400x280")
            welcome_window.resizable(False, False) 
            screen_width = welcome_window.winfo_screenwidth()
            screen_height = welcome_window.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 280) // 2
            welcome_window.geometry(f"+{x}+{y}")
            welcome_window.attributes("-topmost", True)

            # Cargar imagen
            image = Image.open("imgs/welcome_image.png")
            image = image.resize((200, 150))
            photo = ImageTk.PhotoImage(image)
            image_label = customtkinter.CTkLabel(master=welcome_window, text="", image=photo)  # type: ignore
            image_label.image = photo  # type: ignore
            image_label.pack()

            # Mostrar mensaje
            message_text = "Sea bienvenido/a a la herramienta de administración de inventario que le permitirá gestionar sus almacenes de manera eficiente utilizando una base de datos PostgreSQL de forma local o remota."
            message_label = customtkinter.CTkLabel(master=welcome_window, text=message_text, wraplength=300,
                                                   font=customtkinter.CTkFont(size=15))
            message_label.pack()

        welcome_window()

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0) # type: ignore
        self.grid_rowconfigure((0, 1, 2), weight=1) # type: ignore

        # crear subdirectorio almacenes si no existe
        if not os.path.exists("almacenes"):
            os.makedirs("almacenes")

        # Sección lista de almacenes
        self.lista_almacenes = customtkinter.CTkScrollableFrame(self, label_text="Lista de Almacenes", width=650,
                                                                height=300)
        self.lista_almacenes.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.lista_almacenes.place(relx=0.6, rely=0.5, anchor=customtkinter.CENTER)
        self.listar_almacenes()

    def listar_almacenes(self):
        config_files = glob.glob("almacenes/*.bin")

        for i, config_file in enumerate(config_files):
            almacen_name = os.path.splitext(os.path.basename(config_file))[0]
            almacen_frame = customtkinter.CTkFrame(master=self.lista_almacenes, width=200, height=50)
            almacen_frame.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")
            almacen_label = customtkinter.CTkLabel(master=almacen_frame, text=almacen_name, fg_color="#505050",
                                                   corner_radius=6, font=customtkinter.CTkFont(size=15, weight="bold"))
            almacen_label.grid(row=0, column=0, padx=0)
            button_frame = customtkinter.CTkFrame(master=almacen_frame)
            button_frame.grid(row=0, column=1, padx=5)
            self.connect_button = customtkinter.CTkButton(master=button_frame, text="Conectar", fg_color="#28a745",
                                                          hover_color="dark green", command=lambda
                    almacen_name=almacen_name: connect_button_event(almacen_name))
            self.connect_button.grid(row=0, column=0, padx=5)
            self.delete_button = customtkinter.CTkButton(master=button_frame, text="Eliminar", fg_color="#dd1327",
                                                         hover_color="dark red",
                                                         command=lambda almacen_name=almacen_name: delete_button_event(
                                                             self, almacen_name))
            self.delete_button.grid(row=0, column=2, padx=5)

            def connect_button_event(almacen_name):
                config_file_path = f"almacenes/{almacen_name}.bin"
                if os.path.exists(config_file_path):
                    with open(config_file_path, "r") as file:
                        host = file.readline().strip()
                        database = file.readline().strip()
                        user = file.readline().strip()
                        password = file.readline().strip()
                        try:
                            connection = psycopg2.connect(
                                host=host,
                                database=database,
                                user=user,
                                password=password
                            )

                            success_window = customtkinter.CTkToplevel()
                            success_window.geometry("400x200")
                            success_window.title("CONEXIÓN EXITOSA")
                            success_window.resizable(False, False) 
                            screen_width = success_window.winfo_screenwidth()
                            screen_height = success_window.winfo_screenheight()
                            x = (screen_width - 400) // 2
                            y = (screen_height - 200) // 2
                            success_window.geometry(f"+{x}+{y}")
                            success_window.attributes("-topmost", True)
                            success_image = Image.open("imgs/connect_success.png")
                            success_image = success_image.resize((100, 100))
                            photo = ImageTk.PhotoImage(success_image)
                            success_label = customtkinter.CTkLabel(master=success_window, text="",
                                                                   image=photo)  # type: ignore
                            success_label.image = photo  # type: ignore
                            success_label.pack()
                            # Mostrar mensaje de éxito
                            success_text = "Conexión exitosa con la base de datos. Pulse el botón para continuar."
                            success_label = customtkinter.CTkLabel(master=success_window, text=success_text,
                                                                   wraplength=300, font=customtkinter.CTkFont(size=15))
                            success_label.pack()
                            CTkButton(master=success_window, text="ACCEDER", fg_color="#28a745",
                                      hover_color="dark green",
                                      command=lambda: cargar_db(success_window, connection)).pack(expand=True,
                                                                                                  pady=(10, 5), padx=20)

                        except OperationalError as e:

                            error_window = customtkinter.CTkToplevel()
                            error_window.geometry("400x250")
                            error_window.title("ERROR")
                            error_window.resizable(False, False) 
                            screen_width = error_window.winfo_screenwidth()
                            screen_height = error_window.winfo_screenheight()
                            x = (screen_width - 400) // 2
                            y = (screen_height - 250) // 2
                            error_window.geometry(f"+{x}+{y}")
                            error_window.attributes("-topmost", True)
                            error_image = Image.open("imgs/connect_error.png")
                            error_image = error_image.resize((100, 100))
                            photo = ImageTk.PhotoImage(error_image)
                            error_label = customtkinter.CTkLabel(master=error_window, text="",
                                                                 image=photo)  # type: ignore
                            error_label.image = photo  # type: ignore
                            error_label.pack()

                            # Mostrar mensaje de error
                            error_text = "No se pudo establecer conexión con el servidor. Por favor, verifique los parámetros de conexión ingresados e intente nuevamente."
                            error_label = customtkinter.CTkLabel(master=error_window, text=error_text, wraplength=300,
                                                                 font=customtkinter.CTkFont(size=15))
                            error_label.pack()
                            CTkButton(master=error_window, text="REINTENTAR",
                                      command=lambda: connect_error_button_event()).pack(expand=True, pady=10, padx=20)

                            def connect_error_button_event():
                                error_window.destroy()

                            print(e)
                else:
                    print(f"Configuration file for {almacen_name} does not exist.")

        # Crear barra lateral con sus botones
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="ALMACENES",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.update_button = customtkinter.CTkButton(self.sidebar_frame, text="ACTUALIZAR LISTA",
                                                     command=self.update_button_event)
        self.update_button.grid(row=1, column=0, padx=20, pady=10)
        self.new_button = customtkinter.CTkButton(self.sidebar_frame, text="NUEVO", command=new_button_event)
        self.new_button.grid(row=2, column=0, padx=20, pady=10)

    def update_button_event(self):
        for widget in self.lista_almacenes.winfo_children():
            widget.destroy()
        self.listar_almacenes()

    # Ventana para cargar la base de datos e interactuar con ella


def cargar_db(success_window, connection):
    cursor = connection.cursor()
    success_window.destroy()
    db_window = customtkinter.CTkToplevel()
    db_window.title("ALMACÉN")
    db_window.geometry("1200x600")
    db_window.resizable(False, False) 
    screen_width = db_window.winfo_screenwidth()
    screen_height = db_window.winfo_screenheight()
    x = (screen_width - 1280) // 2
    y = (screen_height - 600) // 2
    db_window.geometry(f"+{x}+{y}")
    db_window.attributes("-topmost", True)

    # Barra lateral con las diferentes opciones
    sidebar_frame = CTkFrame(master=db_window, width=230, height=600, corner_radius=0)
    sidebar_frame.grid(row=0, column=0, sticky="ns")
    sidebar_frame.pack_propagate(0)  # type: ignore
    option_label = customtkinter.CTkLabel(master=sidebar_frame, text="SELECCIONE UNA OPCIÓN: ",
                                          font=customtkinter.CTkFont(size=15))
    option_label.pack(side="top", padx=20, pady=(10, 10))
    update_button = customtkinter.CTkButton(master=sidebar_frame, text="ACTUALIZAR LISTADO",
                                            command=lambda: update_product_button_event())
    update_button.pack(side="top", padx=20, pady=10)
    button1 = customtkinter.CTkButton(master=sidebar_frame, text="NUEVA CATEGORIA",
                                      command=lambda: category_button_event(db_window, cursor))
    button1.pack(side="top", padx=20, pady=10)
    button2 = customtkinter.CTkButton(master=sidebar_frame, text="NUEVO PRODUCTO",
                                      command=lambda: new_product_button_event(db_window, cursor))
    button2.pack(side="top", padx=20, pady=10)
    button3 = customtkinter.CTkButton(master=sidebar_frame, text="ABASTECER PRODUCTO",
                                      command=lambda: refill_product_button_event(db_window, cursor))
    button3.pack(side="top", padx=20, pady=10)
    button4 = customtkinter.CTkButton(master=sidebar_frame, text="REGISTRAR COMPRA", fg_color="#28a745",
                                      hover_color="dark green", command=lambda: registrar_compra(db_window, cursor))
    button4.pack(side="top", padx=20, pady=10)
    button5 = customtkinter.CTkButton(master=sidebar_frame, text="HISTORIAL DE COMPRAS", fg_color="#28a745",
                                      hover_color="dark green", command=lambda: historial_compras(db_window, cursor))
    button5.pack(side="top", padx=20, pady=10)
    button6 = customtkinter.CTkButton(master=sidebar_frame, text="GUARDAR Y SALIR", command=lambda: exit(cursor))
    button6.pack(side="top", padx=20, pady=10)
    filter_label = customtkinter.CTkLabel(master=sidebar_frame, text="ORDENAR PRODUCTOS: ",
                                          font=customtkinter.CTkFont(size=13))
    filter_label.pack(side="bottom", padx=20, pady=(10, 10))
    filter_label.place(relx=0.5, rely=0.84, anchor=customtkinter.CENTER)

    filter_options = customtkinter.CTkOptionMenu(master=sidebar_frame, dynamic_resizing=False,
                                                 values=["ID", "CATEGORÍA", "NOMBRE", "PRECIO (€)", "FECHA VENCIMIENTO",
                                                         "STOCK"])
    filter_options.pack(side="bottom", padx=20, pady=50)
    filter_options.configure(command=lambda: update_table(cursor))


    def registrar_compra(db_window, cursor):
        db_window.attributes("-topmost", False)
        # Ventana para registrar una nueva compra
        registrar_compra = customtkinter.CTkToplevel()
        registrar_compra.geometry("600x400")
        registrar_compra.resizable(False, False) 
        screen_width = registrar_compra.winfo_screenwidth()
        screen_height = registrar_compra.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        registrar_compra.geometry(f"+{x}+{y}")
        registrar_compra.title("REGISTRAR COMPRA")
        registrar_compra.attributes("-topmost", True)
        CTkLabel(master=registrar_compra, text="INGRESE LOS DETALLES DE LA COMPRA",
                 font=customtkinter.CTkFont(size=18, weight="bold"), justify="center").pack(expand=True, pady=(15, 5),
                                                                                            padx=(20, 20))
        nombre_producto = CTkEntry(master=registrar_compra, placeholder_text="Nombre del producto", width=300)
        nombre_producto.pack(expand=True, pady=5, padx=20)
        cantidad_compra = CTkEntry(master=registrar_compra, placeholder_text="Cantidad", width=300)
        cantidad_compra.pack(expand=True, pady=5, padx=20)
        nombre_cliente = CTkEntry(master=registrar_compra, placeholder_text="Nombre del cliente", width=300)
        nombre_cliente.pack(expand=True, pady=5, padx=20)
        CTkButton(master=registrar_compra, text="PROCEDER", fg_color="#28a745", hover_color="dark green",
                  command=lambda: registrar_compra_button(registrar_compra, cursor, nombre_producto.get(), cantidad_compra.get(), nombre_cliente.get())).pack(expand=True, pady=5, padx=20)  # type: ignore
        CTkButton(master=registrar_compra, text="CANCELAR", fg_color="#dd1327", hover_color="dark red", command=registrar_compra.destroy).pack(expand=True, pady=5, padx=20)

        def registrar_compra_button(registrar_compra, cursor, nombre_producto, cantidad_compra, nombre_cliente):
            registrar_compra.attributes("-topmost", False)
            try:
                nombre_producto_compra, cantidad_compra, nombre_cliente = nombre_producto, int(
                    cantidad_compra), nombre_cliente

                cursor.execute("SELECT precio_unidad, cantidad_stock FROM PRODUCTOS WHERE nombre_producto = %s",
                               (nombre_producto_compra,))
                resultado = cursor.fetchone()
                precio_unidad, cantidad_stock = resultado
                if cantidad_compra > cantidad_stock:
                    raise Exception("La cantidad de compra es mayor que la cantidad en stock.")

                precio_total_compra = cantidad_compra * precio_unidad
                fecha_compra = date.today()
                hora_compra = datetime.now().time()

                cursor.execute("""
                    INSERT INTO COMPRAS (nombre_producto_compra, cantidad_compra, precio_unidad, precio_total_compra, nombre_cliente, fecha_compra, hora_compra)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (nombre_producto_compra, cantidad_compra, precio_unidad, precio_total_compra, nombre_cliente,
                      fecha_compra, hora_compra))

                nuevo_stock = cantidad_stock - cantidad_compra
                cursor.execute("""
                    UPDATE PRODUCTOS
                    SET cantidad_stock = %s
                    WHERE nombre_producto = %s
                """, (nuevo_stock, nombre_producto_compra))

                success_window = customtkinter.CTkToplevel()
                success_window.geometry("400x350")
                success_window.title("COMPRA REGISTRADA CON ÉXITO")
                success_window.resizable(False, False) 
                screen_width = success_window.winfo_screenwidth()
                screen_height = success_window.winfo_screenheight()
                x = (screen_width - 400) // 2
                y = (screen_height - 350) // 2
                success_window.geometry(f"+{x}+{y}")
                success_window.attributes("-topmost", True)
                success_image = Image.open("imgs/connect_success.png")
                success_image = success_image.resize((100, 100))
                photo = ImageTk.PhotoImage(success_image)
                success_label = customtkinter.CTkLabel(master=success_window, text="", image=photo)  # type: ignore
                success_text = "INFORMACIÓN DE LA COMPRA: \n\n" + "Producto: " + nombre_producto_compra + "\n" + "Cantidad: " + str(
                    cantidad_compra) + "\n" + "Precio por unidad (€): " + str(
                    precio_unidad) + "\n" + "Precio total (€): " + str(
                    precio_total_compra) + "\n" + "Cliente: " + nombre_cliente + "\n" + "Fecha: " + str(
                    fecha_compra) + "\n" + "Hora: " + str(
                    hora_compra) + "\n\n" + "La compra ha sido registrada con éxito."
                success_label = customtkinter.CTkLabel(master=success_window, text=success_text, wraplength=300,
                                                       font=customtkinter.CTkFont(size=15), pady=30)  # type: ignore
                success_label.pack()

                success_label.image = photo  # type: ignore
                success_label.pack()
                # Mostrar mensaje de éxito
                success_label.pack()
                CTkButton(master=success_window, text="CONTINUAR", fg_color="#28a745", hover_color="dark green",
                          command=lambda: continuar(cursor)).pack(expand=True, pady=(10, 5), padx=20)

                def continuar(cursor):
                    cursor.connection.commit()
                    success_window.destroy()
                    registrar_compra.destroy()

            except (Exception, psycopg2.Error) as error:
                print("Error al registrar la compra:", error)
                error_window = customtkinter.CTkToplevel()
                error_window.geometry("400x250")
                error_window.title("ERROR")
                error_window.resizable(False, False) 
                screen_width = error_window.winfo_screenwidth()
                screen_height = error_window.winfo_screenheight()
                x = (screen_width - 400) // 2
                y = (screen_height - 250) // 2
                error_window.geometry(f"+{x}+{y}")
                error_window.attributes("-topmost", True)
                error_image = Image.open("imgs/connect_error.png")
                error_image = error_image.resize((100, 100))
                photo = ImageTk.PhotoImage(error_image)
                error_label = customtkinter.CTkLabel(master=error_window, text="", image=photo)  # type: ignore
                error_label.image = photo  # type: ignore
                error_label.pack()

                # Mostrar mensaje de error
                error_text = "Error al procesar la compra, intente nuevamente."
                error_label = customtkinter.CTkLabel(master=error_window, text=error_text, wraplength=300,
                                                     font=customtkinter.CTkFont(size=15))
                error_label.pack()
                CTkButton(master=error_window, text="REINTENTAR", command=lambda: reintentar()).pack(expand=True,
                                                                                                     pady=10, padx=20)

                def reintentar():
                    error_window.destroy()

    def historial_compras(db_window, cursor):
        db_window.attributes("-topmost", False)
        # Ventana para mostrar el historial de compras
        historial_compras = customtkinter.CTkToplevel()
        historial_compras.geometry("1050x600")
        historial_compras.resizable(False, False) 
        historial_compras.title("HISTORIAL DE COMPRAS")
        screen_width = historial_compras.winfo_screenwidth()
        screen_height = historial_compras.winfo_screenheight()
        x = (screen_width - 1050) // 2
        y = (screen_height - 600) // 2
        historial_compras.geometry(f"+{x}+{y}")
        historial_compras.attributes("-topmost", True)

        # Sección historial de compras
        cursor.execute(f"SELECT * FROM COMPRAS ORDER BY fecha_compra")
        compras = cursor.fetchall()
        column_names = ["ID", "Producto", "Cantidad", "Precio por unidad (€)", "Precio total (€)", "Nombre cliente", "Fecha",
                        "Hora"]
        table_data = [list(compra) for compra in compras]
        table_data.insert(0, column_names)
        productos_frame = customtkinter.CTkScrollableFrame(master=historial_compras, label_text="COMPRAS", width=1000,
                                                           height=500)
        productos_frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        table = CTkTable(master=productos_frame, values=table_data)
        table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        table.pack(expand=True)

    def check_stock(cursor):
        cursor.execute("SELECT nombre_producto FROM productos WHERE cantidad_stock <= 10")
        productos = cursor.fetchall()
        if productos:
            check_stock = customtkinter.CTkToplevel()
            check_stock.title("ATENCIÓN")
            check_stock.geometry("400x250")
            check_stock.resizable(False, False) 
            check_stock.attributes("-topmost", True)
            screen_width = check_stock.winfo_screenwidth()
            screen_height = check_stock.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 150) // 2
            check_stock.geometry(f"+{x}+{y}")
            # Cargar imagen
            image = Image.open("imgs/connect_error.png")
            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            image_label = customtkinter.CTkLabel(master=check_stock, text="", image=photo)  # type: ignore
            image_label.image = photo  # type: ignore
            image_label.pack()
            message = (
                "Los siguientes productos se encuentran escasos en stock. Por favor, reabastézcalos lo antes posible:")
            message_label = customtkinter.CTkLabel(master=check_stock, text=message, wraplength=300,
                                                   font=customtkinter.CTkFont(size=15), pady=10)
            message_label.pack()
            message2 = "\n".join(producto[0] for producto in productos)
            message_label2 = customtkinter.CTkLabel(master=check_stock, text=message2, wraplength=300,
                                                    font=customtkinter.CTkFont(size=15), pady=10)
            message_label2.pack()

    check_stock(cursor)

    def exit(cursor):
        cursor.close()
        connection.close()
        db_window.destroy()

    def update_table(cursor):

        selected_option = filter_options.get()
        option_to_column = {
            "ID": "id",
            "CATEGORÍA": "categoria",
            "NOMBRE": "nombre_producto",
            "PRECIO (€)": "precio_unidad",
            "FECHA VENCIMIENTO": "fecha_vencimiento",
            "STOCK": "cantidad_stock"
        }
        selected_column = option_to_column[selected_option]

        # Ejecutar consulta SQL para obtener todos los datos de la tabla PRODUCTOS, ordenados según la opción seleccionada
        cursor.execute(f"SELECT * FROM PRODUCTOS ORDER BY {selected_column}")
        productos = cursor.fetchall()

        # Sección mostrar productos
        column_names = ["ID", "Categoría", "Nombre del producto", "Cantidad en stock", "Precio por unidad (€)",
                        "Fecha de vencimiento"]
        table_data = [list(producto) for producto in productos]
        table_data.insert(0, column_names)
        productos_frame = customtkinter.CTkScrollableFrame(master=db_window, label_text="PRODUCTOS", width=900,
                                                           height=500)
        productos_frame.place(relx=0.6, rely=0.5, anchor=customtkinter.CENTER)
        table = CTkTable(master=productos_frame, values=table_data)
        table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        table.pack(expand=True)

    update_table(cursor)

    def update_product_button_event():
        update_table(cursor)

    def refill_product_button_event(db_window, cursor):
        db_window.attributes("-topmost", False)

        # Ventana para reabastecer un producto
        refill_product = customtkinter.CTkToplevel()
        refill_product.geometry("300x300")
        refill_product.resizable(False, False) 
        screen_width = refill_product.winfo_screenwidth()
        screen_height = refill_product.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 300) // 2
        refill_product.geometry(f"+{x}+{y}")
        refill_product.attributes("-topmost", True)
        refill_product.title("ABASTECER PRODUCTO EXISTENTE")

        CTkLabel(master=refill_product, text="ABASTECER PRODUCTO", font=customtkinter.CTkFont(size=18, weight="bold"),
                 justify="center").pack(expand=True, pady=(15, 5), padx=(20, 20))
        product_id = CTkEntry(master=refill_product, placeholder_text="ID del producto a abastecer", width=300)
        product_id.pack(expand=True, pady=5, padx=20)
        cantidad = CTkEntry(master=refill_product, placeholder_text="Cantidad a abastecer", width=300)
        cantidad.pack(expand=True, pady=5, padx=20)

        CTkButton(master=refill_product, text="ABASTECER", fg_color="#28a745", hover_color="dark green",
                  command=lambda: refill_button(cursor, product_id.get(), cantidad.get())).pack(expand=True, pady=5,
                                                                                                padx=20)  # type: ignore
        CTkButton(master=refill_product, text="CANCELAR", fg_color="#dd1327", hover_color="dark red",
                  command=refill_product.destroy).pack(expand=True, pady=5, padx=20)

        def refill_button(cursor, product_id, cantidad):
            try:
                id = product_id
                cantidad_nueva = int(cantidad)

                cursor.execute("SELECT cantidad_stock FROM PRODUCTOS WHERE id = %s", (id,))
                cantidad_actual = cursor.fetchone()

                nueva_cantidad_total = cantidad_actual[0] + cantidad_nueva

                cursor.execute("""
                UPDATE PRODUCTOS
                SET cantidad_stock = %s
                WHERE id = %s
            """, (nueva_cantidad_total, product_id))

                success_window = customtkinter.CTkToplevel()
                success_window.geometry("300x300")
                success_window.title("ABASTECIDO CON ÉXITO")
                success_window.resizable(False, False) 
                success_image = Image.open("imgs/connect_success.png")
                success_image = success_image.resize((100, 100))
                photo = ImageTk.PhotoImage(success_image)
                success_label = customtkinter.CTkLabel(master=success_window, text="", image=photo)  # type: ignore
                success_label.image = photo  # type: ignore
                success_label.pack()
                # Mostrar mensaje de éxito
                success_label.pack()
                CTkButton(master=success_window, text="CONTINUAR", fg_color="#28a745", hover_color="dark green",
                          command=lambda: continuar(cursor)).pack(expand=True, pady=(10, 5), padx=20)

                def continuar(cursor):
                    cursor.connection.commit()
                    success_window.destroy()
                    refill_product.destroy()

            except (Exception, psycopg2.Error) as error:
                print("Error al reabastecer:", error)
                error_window = customtkinter.CTkToplevel()
                error_window.geometry("400x250")
                error_window.title("ERROR")
                error_window.resizable(False, False) 

                error_image = Image.open("imgs/connect_error.png")
                error_image = error_image.resize((100, 100))
                photo = ImageTk.PhotoImage(error_image)
                error_label = customtkinter.CTkLabel(master=error_window, text="", image=photo)  # type: ignore
                error_label.image = photo  # type: ignore
                error_label.pack()

                # Mostrar mensaje de error
                error_text = "Error al abastecer el producto, intente nuevamente."
                error_label = customtkinter.CTkLabel(master=error_window, text=error_text, wraplength=300,
                                                     font=customtkinter.CTkFont(size=15))
                error_label.pack()
                CTkButton(master=error_window, text="REINTENTAR", command=lambda: reintentar()).pack(expand=True,
                                                                                                     pady=10, padx=20)

                def reintentar():
                    error_window.destroy()

    def category_button_event(db_window, cursor):
        db_window.attributes("-topmost", False)
        new_category = customtkinter.CTkToplevel()
        new_category.geometry("300x300")
        new_category.resizable(False, False) 
        screen_width = new_category.winfo_screenwidth()
        screen_height = new_category.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 300) // 2
        new_category.geometry(f"+{x}+{y}")
        new_category.attributes("-topmost", True)
        new_category.title("INSERTAR NUEVA CATEGORÍA")

        CTkLabel(master=new_category, text="NUEVA CATEGORÍA", font=customtkinter.CTkFont(size=18, weight="bold"),
                 justify="center").pack(expand=True, pady=(15, 5), padx=(20, 20))
        nombre_categoria = CTkEntry(master=new_category, placeholder_text="Nombre de la categoría", width=300)
        nombre_categoria.pack(expand=True, pady=5, padx=20)
        CTkButton(master=new_category, text="GUARDAR CATEGORÍA", fg_color="#28a745", hover_color="dark green",
                  command=lambda: guardar_categoria_button(new_category, cursor, nombre_categoria.get())).pack(expand=True, pady=5,
                                                                                                 padx=20)  # type: ignore
        CTkButton(master=new_category, text="CANCELAR", fg_color="#dd1327", hover_color="dark red",
                  command=new_category.destroy).pack(expand=True, pady=5, padx=20)

        def guardar_categoria_button(new_category, cursor, nombre_categoria):
            new_category.attributes("-topmost", False)

            try:
                nombre_categoria = nombre_categoria

                cursor.execute("""
                    INSERT INTO CATEGORIAS (nombre_categoria)
                    VALUES (%s)
                """, (nombre_categoria,))

                success_window = customtkinter.CTkToplevel()
                success_window.geometry("400x200")
                success_window.title("GUARDADO CON ÉXITO")
                success_window.resizable(False, False) 
                success_image = Image.open("imgs/connect_success.png")
                success_image = success_image.resize((100, 100))
                screen_width = success_window.winfo_screenwidth()
                screen_height = success_window.winfo_screenheight()
                x = (screen_width - 400) // 2
                y = (screen_height - 200) // 2
                success_window.geometry(f"+{x}+{y}")
                success_window.attributes("-topmost", True)
                photo = ImageTk.PhotoImage(success_image)
                success_label = customtkinter.CTkLabel(master=success_window, text="", image=photo)  # type: ignore
                success_label.image = photo  # type: ignore
                success_label.pack()
                # Mostrar mensaje de éxito
                success_label.pack()
                CTkButton(master=success_window, text="CONTINUAR", fg_color="#28a745", hover_color="dark green",
                          command=lambda: continuar(cursor)).pack(expand=True, pady=(10, 5), padx=20)

                def continuar(cursor):
                    cursor.connection.commit()
                    success_window.destroy()
                    new_category.destroy()

            except (Exception, psycopg2.Error) as error:
                print("Error al crear la categoría:", error)
                error_window = customtkinter.CTkToplevel()
                error_window.geometry("400x250")
                error_window.title("ERROR")
                error_window.resizable(False, False) 
                screen_width = error_window.winfo_screenwidth()
                screen_height = error_window.winfo_screenheight()
                x = (screen_width - 400) // 2
                y = (screen_height - 250) // 2
                error_window.geometry(f"+{x}+{y}")
                error_window.attributes("-topmost", True)
                error_image = Image.open("imgs/connect_error.png")
                error_image = error_image.resize((100, 100))
                photo = ImageTk.PhotoImage(error_image)
                error_label = customtkinter.CTkLabel(master=error_window, text="", image=photo)  # type: ignore
                error_label.image = photo  # type: ignore
                error_label.pack()

                # Mostrar mensaje de error
                error_text = "Error al crear la categoría, intente nuevamente."
                error_label = customtkinter.CTkLabel(master=error_window, text=error_text, wraplength=300,
                                                     font=customtkinter.CTkFont(size=15))
                error_label.pack()
                CTkButton(master=error_window, text="REINTENTAR", command=lambda: reintentar()).pack(expand=True,
                                                                                                     pady=10, padx=20)

                def reintentar():
                    error_window.destroy()

    def new_product_button_event(db_window, cursor):
        db_window.attributes("-topmost", False)

        # Ventana para insertar un nuevo producto
        new_product = customtkinter.CTkToplevel()
        new_product.geometry("600x400")
        new_product.resizable(False, False) 
        new_product.title("INSERTAR NUEVO PRODUCTO")
        screen_width = new_product.winfo_screenwidth()
        screen_height = new_product.winfo_screenheight()
        x = (screen_width - 680) // 2
        y = (screen_height - 400) // 2
        new_product.geometry(f"+{x}+{y}")
        new_product.attributes("-topmost", True)

        CTkLabel(master=new_product, text="INGRESE LOS DETALLES DEL PRODUCTO",
                 font=customtkinter.CTkFont(size=18, weight="bold"), justify="center").pack(expand=True, pady=(15, 5),
                                                                                            padx=(20, 20))
        nombre_producto = CTkEntry(master=new_product, placeholder_text="Nombre del producto", width=300)
        nombre_producto.pack(expand=True, pady=5, padx=20)
        cantidad_stock = CTkEntry(master=new_product, placeholder_text="Cantidad", width=300)
        cantidad_stock.pack(expand=True, pady=5, padx=20)
        categoria = CTkEntry(master=new_product, placeholder_text="Categoría", width=300)
        categoria.pack(expand=True, pady=5, padx=20)
        precio_unidad = CTkEntry(master=new_product, placeholder_text="Precio por unidad (€)", width=300)
        precio_unidad.pack(expand=True, pady=5, padx=20)
        fecha_vencimiento = CTkEntry(master=new_product, placeholder_text="Fecha de vencimiento (YYYY-MM-DD)",
                                     width=300)
        fecha_vencimiento.pack(expand=True, pady=5, padx=20)
        CTkButton(master=new_product, text="GUARDAR PRODUCTO", fg_color="#28a745", hover_color="dark green",
                  command=lambda: guardar_producto_button(new_product, cursor, nombre_producto.get(), categoria.get(),
                                                          cantidad_stock.get(), precio_unidad.get(),
                                                          fecha_vencimiento.get())).pack(expand=True, pady=5,
                                                                                         padx=20)  # type: ignore
        CTkButton(master=new_product, text="CANCELAR", fg_color="#dd1327", hover_color="dark red",
                  command=new_product.destroy).pack(expand=True, pady=5, padx=20)

        def guardar_producto_button(new_product, cursor, nombre_producto, categoria, cantidad_stock, precio_unidad,
                                    fecha_vencimiento):
            new_product.attributes("-topmost", False)
            try:
                nombre_producto, categoria, cantidad_stock, precio_unidad, fecha_vencimiento = nombre_producto, categoria, cantidad_stock, precio_unidad, fecha_vencimiento

                cursor.execute("""
                    INSERT INTO PRODUCTOS (nombre_producto, categoria, cantidad_stock, precio_unidad, fecha_vencimiento)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre_producto, categoria, cantidad_stock, precio_unidad, fecha_vencimiento))

                success_window = customtkinter.CTkToplevel()
                success_window.geometry("400x300")
                success_window.title("GUARDADO CON ÉXITO")
                success_window.resizable(False, False) 
                success_image = Image.open("imgs/connect_success.png")
                success_image = success_image.resize((100, 100))
                screen_width = success_window.winfo_screenwidth()
                screen_height = success_window.winfo_screenheight()
                x = (screen_width - 400) // 2
                y = (screen_height - 300) // 2
                success_window.geometry(f"+{x}+{y}")
                success_window.attributes("-topmost", True)
                photo = ImageTk.PhotoImage(success_image)
                success_label = customtkinter.CTkLabel(master=success_window, text="", image=photo)  # type: ignore
                success_label.image = photo  # type: ignore
                success_label.pack()
                # Mostrar mensaje de éxito
                success_label.pack()
                CTkButton(master=success_window, text="CONTINUAR", fg_color="#28a745", hover_color="dark green",
                          command=lambda: continuar(cursor)).pack(expand=True, pady=(10, 5), padx=20)

                def continuar(cursor):
                    cursor.connection.commit()
                    success_window.destroy()
                    new_product.destroy()

            except (Exception, psycopg2.Error) as error:
                print("Error al crear el producto:", error)
                error_window = customtkinter.CTkToplevel()
                error_window.geometry("400x250")
                error_window.title("ERROR")
                error_window.resizable(False, False) 
                screen_width = error_window.winfo_screenwidth()
                screen_height = error_window.winfo_screenheight()
                x = (screen_width - 400) // 2
                y = (screen_height - 250) // 2
                error_window.geometry(f"+{x}+{y}")
                error_window.attributes("-topmost", True)

                error_image = Image.open("imgs/connect_error.png")
                error_image = error_image.resize((100, 100))
                photo = ImageTk.PhotoImage(error_image)
                error_label = customtkinter.CTkLabel(master=error_window, text="", image=photo)  # type: ignore
                error_label.image = photo  # type: ignore
                error_label.pack()

                # Mostrar mensaje de error
                error_text = "No se pudo guardar los datos del producto. Por favor, verifique los parámetros e intente nuevamente."
                error_label = customtkinter.CTkLabel(master=error_window, text=error_text, wraplength=300,
                                                     font=customtkinter.CTkFont(size=15))
                error_label.pack()
                CTkButton(master=error_window, text="REINTENTAR", command=lambda: reintentar()).pack(expand=True,
                                                                                                     pady=10, padx=20)

                def reintentar():
                    error_window.destroy()


def delete_button_event(self, almacen_name):
    config_file_path = f"almacenes/{almacen_name}.bin"
    if os.path.exists(config_file_path):
        os.remove(config_file_path)

        delete_success = customtkinter.CTk()
        delete_success.geometry("400x150")
        delete_success.title("ELIMINAR")
        delete_success.resizable(False, False) 

        def ok_function():
            delete_success.destroy()
            for widget in self.lista_almacenes.winfo_children():
                widget.destroy()
            self.listar_almacenes()

        CTkLabel(master=delete_success, text="ALMACÉN ELIMINADO", font=customtkinter.CTkFont(size=18, weight="bold"),
                 justify="center").place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)
        button = customtkinter.CTkButton(master=delete_success, text="OK", command=ok_function)
        button.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

    else:
        print(f"Configuration file for {almacen_name} does not exist.")


def new_button_event():
    # Ventana para crear un nuevo almacén
    new_window = customtkinter.CTkToplevel()
    new_window.geometry("600x400")
    new_window.resizable(False, False) 
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x = (screen_width - 600) // 2
    y = (screen_height - 400) // 2
    new_window.geometry(f"+{x}+{y}")
    new_window.attributes("-topmost", True)
    new_window.title("NUEVO ALMACÉN")
    nuevo = CTkFrame(master=new_window)
    nuevo.grid(row=1, column=1)
    nuevo.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    CTkLabel(master=nuevo, text="INGRESE LOS PARÁMETROS DE CONEXIÓN DEL SERVIDOR",
             font=customtkinter.CTkFont(size=18, weight="bold"), justify="center").pack(expand=True, pady=(15, 5),
                                                                                        padx=(20, 20))
    CTkLabel(master=nuevo,
             text="Debe conectarse a una base de datos previamente creada la cual no contenga información almacenada o podrían ocurrir errores. Proceder con precaución...",
             wraplength=500, font=customtkinter.CTkFont(size=15, weight="normal"), justify="center").pack(expand=True,
                                                                                                          pady=(0, 15),
                                                                                                          padx=(25, 25))
    name = CTkEntry(master=nuevo, placeholder_text="Nombre del almacén", width=300)
    name.pack(expand=True, pady=5, padx=20)
    host = CTkEntry(master=nuevo, placeholder_text="Host", width=300)
    host.pack(expand=True, pady=5, padx=20)
    database = CTkEntry(master=nuevo, placeholder_text="Database", width=300)
    database.pack(expand=True, pady=5, padx=20)
    user = CTkEntry(master=nuevo, placeholder_text="User", width=300)
    user.pack(expand=True, pady=5, padx=20)
    password = CTkEntry(master=nuevo, placeholder_text="Password", width=300)
    password.pack(expand=True, pady=5, padx=20)
    CTkButton(master=nuevo, text="PROBAR CONEXIÓN", fg_color="#28a745", hover_color="dark green",
              command=lambda: connect_button_event_new(new_window, name.get(), host.get(), database.get(), user.get(),
                                                       password.get())).pack(expand=True, pady=5,
                                                                             padx=20)  # type: ignore
    CTkButton(master=nuevo, text="CANCELAR", fg_color="#dd1327", hover_color="dark red",
              command=new_window.destroy).pack(expand=True, pady=5, padx=20)

    # Intentar conexión con la base de datos
    def connect_button_event_new(new_window, name, host, database, user, password):
        new_window.attributes("-topmost", False)

        try:
            connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            success_window = customtkinter.CTkToplevel()
            success_window.geometry("400x300")
            success_window.title("CONEXIÓN EXITOSA")
            success_window.resizable(False, False) 
            success_image = Image.open("imgs/connect_success.png")
            success_image = success_image.resize((100, 100))
            screen_width = success_window.winfo_screenwidth()
            screen_height = success_window.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 300) // 2
            success_window.geometry(f"+{x}+{y}")
            success_window.attributes("-topmost", True)
            photo = ImageTk.PhotoImage(success_image)
            success_label = customtkinter.CTkLabel(master=success_window, text="", image=photo)  # type: ignore
            success_label.image = photo  # type: ignore
            success_label.pack()
            # Mostrar mensaje de éxito
            success_text = "Conexión exitosa con la base de datos. Guarde la configuración y acceda a su almacén o descarte los cambios. Acceda a la base de datos desde el menú principal. Pulse el botón ACTUALIZAR LISTA para ver los cambios."
            success_label = customtkinter.CTkLabel(master=success_window, text=success_text, wraplength=300,
                                                   font=customtkinter.CTkFont(size=15))
            success_label.pack()
            CTkButton(master=success_window, text="GUARDAR", fg_color="#28a745", hover_color="dark green",
                      command=lambda: connect_success_button_event()).pack(expand=True, pady=(10, 5), padx=20)
            CTkButton(master=success_window, text="NO GUARDAR", fg_color="#dd1327", hover_color="dark red",
                      command=lambda: connect_success_cancel_button_event()).pack(expand=True, pady=(5, 10), padx=20)
            new_window.destroy()

            def connect_success_button_event():
                success_window.destroy()
                file_path = f"almacenes/{name}.bin"
                with open(file_path, "w") as file:
                    file.write(f'{host}\n')
                    file.write(f'{database}\n')
                    file.write(f'{user}\n')
                    file.write(f'{password}\n')
                    crear_tablas(connection)

            def crear_tablas(connection):
                cursor = connection.cursor()

                # Create table CATEGORIAS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS CATEGORIAS (
                        id SERIAL PRIMARY KEY,
                        nombre_categoria VARCHAR(255) UNIQUE
                    )
                """)

                # Create table PRODUCTOS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PRODUCTOS (
                        id SERIAL PRIMARY KEY,
                        categoria VARCHAR(255) REFERENCES CATEGORIAS(nombre_categoria),
                        nombre_producto VARCHAR(255) UNIQUE,
                        cantidad_stock INTEGER,
                        precio_unidad REAL,
                        fecha_vencimiento DATE
                    )
                """)

                # Create table COMPRAS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS COMPRAS (
                        id SERIAL PRIMARY KEY,
                        nombre_producto_compra VARCHAR(255) REFERENCES PRODUCTOS(nombre_producto),
                        cantidad_compra INTEGER,
                        precio_unidad REAL,
                        precio_total_compra REAL,
                        nombre_cliente VARCHAR(255),
                        fecha_compra DATE,
                        hora_compra TIME
                    )
                """)

                cursor.connection.commit()
                cursor.close()

            def connect_success_cancel_button_event():
                success_window.destroy()

        except OperationalError as e:
            error_window = customtkinter.CTkToplevel()
            error_window.geometry("400x250")
            error_window.title("ERROR")
            error_window.resizable(False, False) 
            screen_width = error_window.winfo_screenwidth()
            screen_height = error_window.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 250) // 2
            error_window.geometry(f"+{x}+{y}")
            error_window.attributes("-topmost", True)
            error_image = Image.open("imgs/connect_error.png")
            error_image = error_image.resize((100, 100))
            photo = ImageTk.PhotoImage(error_image)
            error_label = customtkinter.CTkLabel(master=error_window, text="", image=photo)  # type: ignore
            error_label.image = photo  # type: ignore
            error_label.pack()

            # Mostrar mensaje de error
            error_text = "No se pudo establecer conexión con el servidor. Por favor, verifique los parámetros de conexión ingresados e intente nuevamente."
            error_label = customtkinter.CTkLabel(master=error_window, text=error_text, wraplength=300,
                                                 font=customtkinter.CTkFont(size=15))
            error_label.pack()
            CTkButton(master=error_window, text="REINTENTAR", command=lambda: connect_error_button_event()).pack(
                expand=True, pady=10, padx=20)

            def connect_error_button_event():
                error_window.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()