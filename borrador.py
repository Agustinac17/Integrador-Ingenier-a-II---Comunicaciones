import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
from datetime import datetime
from netmiko import ConnectHandler
from art import text2art

# Crear arte ASCII con la palabra "AgusTik"
ascii_art = text2art("AgusTik")

# Imprimir el arte ASCII
print(ascii_art)

# Datos del dispositivo
router_config = {
    'device_type': 'cisco_ios',
    "host": "R1",
    'username': 'agusti',
    'password': 'agusword',
    'secret': 'tikwordagus',
}

# Directorio donde se guardarán los backups
DIRECTORIO_BACKUPS = "C:/Users/Bangho/GNS3/projects/prueba"


def realizar_backup(router_config, nombre_dispositivo):
    try:
        net_connect = ConnectHandler(**router_config)
        net_connect.enable()

        output = net_connect.send_command('show running-config')

        # Verificar la existencia del directorio
        if not os.path.exists(DIRECTORIO_BACKUPS):
            os.makedirs(DIRECTORIO_BACKUPS)

        fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{DIRECTORIO_BACKUPS}/backup_{fecha_hora}_{nombre_dispositivo}.backup'

        with open(filename, 'w') as file:
            file.write(output)

        net_connect.disconnect()

        print(f'Backup completado y guardado en {filename}')
        messagebox.showinfo('Éxito', f'Backup completado y guardado en {filename}')
    except Exception as e:
        print(f'Error al realizar el backup: {e}')
        messagebox.showerror('Error', f'Error al realizar el backup: {e}')

def cambiar_nombre_equipo(router_config):
    nombre = nombre_equipo.get()
    if nombre:
        try:
            net_connect = ConnectHandler(**router_config)
            net_connect.enable()
            
            command = f"enable" 
            net_connect.send_config_set([command])
            command = f"configure terminal" 
            net_connect.send_config_set([command])
            command = f'hostname {nombre}'
            net_connect.send_config_set([command])
            command = f'exit'
            net_connect.send_config_set([command])
            command = f'write memory'
            net_connect.send_config_set([command])

            net_connect.disconnect()

            messagebox.showinfo('Éxito', 'Se ha cambiado el nombre del equipo correctamente.')
        except Exception as e:
            messagebox.showerror('Error', f'Hubo un error al cambiar el nombre del equipo:\n{e}')
    else:
        messagebox.showwarning('Advertencia', 'Por favor ingresa un nombre para el equipo.')

def agregar_dispositivo():
    nombre = entry_nombre_dispositivo.get()
    ip = entry_ip_dispositivo.get()
    if nombre and ip:
        listbox_dispositivos.insert(tk.END, f"{nombre} ({ip})")
        entry_nombre_dispositivo.delete(0, tk.END)
        entry_ip_dispositivo.delete(0, tk.END)
    else:
        messagebox.showwarning('Advertencia', 'Por favor ingresa el nombre y la IP del dispositivo.')

def eliminar_dispositivo():
    seleccion = listbox_dispositivos.curselection()
    if seleccion:
        listbox_dispositivos.delete(seleccion)
    else:
        messagebox.showwarning('Advertencia', 'Por favor selecciona un dispositivo para eliminar.')

def programar_backup():
    dispositivos = listbox_dispositivos.get(0, tk.END)
    try:
        periodicidad = int(entry_periodicidad.get())
        cantidad_respaldo = int(entry_cantidad_respaldo.get())
    except ValueError:
        messagebox.showerror('Error', 'La periodicidad y la cantidad de respaldos deben ser números enteros.')
        return
    
    for dispositivo in dispositivos:
        nombre_dispositivo = dispositivo.split(' ')[0]
        realizar_backup(router_config, nombre_dispositivo)
        # Aquí deberíamos programar la siguiente ejecución con un scheduler adecuado

    # Limitar la cantidad de backups
    # Aquí deberías añadir la lógica para limitar los archivos de respaldo a la cantidad especificada



""""""
# Ventana principal
root = tk.Tk()
root.title('Gestión de AgusTik RouterOS')
root.config(bg="light pink")  # Establecer el fondo de la ventana
root.geometry('570x550')  # Tamaño de la ventana

# Aplicar un tema visual
style = ThemedStyle(root)
style.theme_use('plastik')  # Puedes probar otros temas como 'equilux', 'clam', 'plastik', etc.

# Cargar y redimensionar la imagen del logo
try:
    logo = Image.open("logoooooo.jpeg")
    logo = logo.resize((100, 100), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo)
    
    # Crear y colocar la etiqueta del logo
    logo_label = ttk.Label(root, image=logo)
    logo_label.grid(row=0, column=0, padx=0, pady=0, sticky=tk.W)
except Exception as e:
    print(f"Error al cargar el logo: {e}")

# Frame para los campos de entrada y botones
frame = ttk.Frame(root, padding="10")
frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

# Campo para ingresar el nombre del equipo
ttk.Label(frame, text="Nombre del equipo:").grid(row=0, column=0, sticky=tk.W)
nombre_equipo = ttk.Entry(frame, width=30)
nombre_equipo.grid(row=0, column=1, sticky=tk.W)

ttk.Button(frame, text="Cambiar nombre del equipo", command=lambda: cambiar_nombre_equipo(router_config)).grid(row=0, column=2, sticky=tk.W)

# Lista de dispositivos
ttk.Label(frame, text="Dispositivos:").grid(row=1, column=0, sticky=tk.W)
listbox_dispositivos = tk.Listbox(frame, height=10, width=50)
listbox_dispositivos.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

# Campo para agregar nuevo dispositivo
ttk.Label(frame, text="Nombre del dispositivo:").grid(row=3, column=0, sticky=tk.W)
entry_nombre_dispositivo = ttk.Entry(frame, width=30)
entry_nombre_dispositivo.grid(row=3, column=1, sticky=tk.W)

ttk.Label(frame, text="IP del dispositivo:").grid(row=4, column=0, sticky=tk.W)
entry_ip_dispositivo = ttk.Entry(frame, width=30)
entry_ip_dispositivo.grid(row=4, column=1, sticky=tk.W)

ttk.Button(frame, text="Agregar dispositivo", command=agregar_dispositivo).grid(row=5, column=1, sticky=tk.W)
ttk.Button(frame, text="Eliminar dispositivo", command=eliminar_dispositivo).grid(row=5, column=2, sticky=tk.W)

# Campo para ingresar la periodicidad del backup
ttk.Label(frame, text="Periodicidad del backup (en minutos):").grid(row=6, column=0, sticky=tk.W)
entry_periodicidad = ttk.Entry(frame, width=30)
entry_periodicidad.grid(row=6, column=1, sticky=tk.W)

# Campo para ingresar la cantidad de backups a mantener
ttk.Label(frame, text="Cantidad de backups a mantener:").grid(row=7, column=0, sticky=tk.W)
entry_cantidad_respaldo = ttk.Entry(frame, width=30)
entry_cantidad_respaldo.grid(row=7, column=1, sticky=tk.W)

ttk.Button(frame, text="Programar backup", command=programar_backup).grid(row=8, column=1, sticky=tk.W)

root.mainloop()
