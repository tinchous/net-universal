#!/usr/bin/env python3
# ==========================================================
# Red Tools
# Herramienta de Diagnóstico de Red
# Multiplataforma: Windows / Linux
#
# DISEÑO:
#  - Header con SO detectado
#  - Columna 1: Categorías (menú)
#  - Columna 2: Acciones (comandos)
#  - Columna 3: Advertencias / explicación
#  - Abajo: salida de comandos
#
# Código comentado nivel "gurí cagado"
#
# Autor: Tino / TinuX SolucioneS
# ==========================================================

import platform
import subprocess
import datetime
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

# ----------------------------------------------------------
# SISTEMA OPERATIVO Y ENCODING
# ----------------------------------------------------------
OS = platform.system()
ENCODING = "cp850" if OS == "Windows" else "utf-8"

# ----------------------------------------------------------
# FUNCIÓN PARA EJECUTAR COMANDOS DEL SISTEMA
# ----------------------------------------------------------
def ejecutar(comando):
    """
    Ejecuta un comando en el sistema y muestra la salida
    en el área inferior (tipo consola).
    """
    salida.insert(tk.END, f"\n> {comando}\n")
    try:
        resultado = subprocess.check_output(
            comando,
            shell=True,
            stderr=subprocess.STDOUT,
            text=True,
            encoding=ENCODING,
            errors="replace"
        )
        salida.insert(tk.END, resultado)
    except subprocess.CalledProcessError as e:
        salida.insert(tk.END, e.output)
    salida.see(tk.END)

# ----------------------------------------------------------
# FUNCIONES DE COMANDOS (ACCIONES REALES)
# ----------------------------------------------------------
def ver_ip(): ejecutar("ipconfig" if OS == "Windows" else "ip a")
def ip_detallada(): ejecutar("ipconfig /all" if OS == "Windows" else "ip a && ip r")

def ping():
    h = simpledialog.askstring("Ping", "IP o dominio:")
    if h: ejecutar(f"ping {h}" if OS == "Windows" else f"ping -c 4 {h}")

def traceroute():
    h = simpledialog.askstring("Traceroute", "IP o dominio:")
    if h: ejecutar("tracert "+h if OS=="Windows" else "traceroute "+h)

def pathping():
    h = simpledialog.askstring("PathPing / MTR", "IP o dominio:")
    if h: ejecutar("pathping "+h if OS=="Windows" else "mtr -r "+h)

def nslookup():
    d = simpledialog.askstring("NSLookup", "Dominio:")
    if d: ejecutar("nslookup "+d)

def conexiones(): ejecutar("netstat -an" if OS=="Windows" else "ss -tulpn")

# ARP
def arp_listar(): ejecutar("arp -a" if OS=="Windows" else "ip neigh")

def arp_borrar():
    if messagebox.askyesno("Cuidado", "Borrar caché ARP puede cortar la red.\n¿Continuar?"):
        ejecutar("arp -d *" if OS=="Windows" else "sudo ip neigh flush all")

# SERVICIOS
def servicios_listar():
    ejecutar("net start" if OS=="Windows"
             else "systemctl list-units --type=service")

def servicio_iniciar():
    s = simpledialog.askstring("Servicio", "Nombre del servicio:")
    if s: ejecutar(f"net start {s}" if OS=="Windows" else f"sudo systemctl start {s}")

def servicio_detener():
    s = simpledialog.askstring("Servicio", "Nombre del servicio:")
    if s: ejecutar(f"net stop {s}" if OS=="Windows" else f"sudo systemctl stop {s}")

# SISTEMA
def hostname_cmd(): ejecutar("hostname")
def mac(): ejecutar("getmac" if OS=="Windows" else "ip link")

# INTERNET
def diagnostico_internet():
    salida.delete(1.0, tk.END)
    ejecutar("ipconfig" if OS=="Windows" else "ip a")
    ejecutar("ping 8.8.8.8" if OS=="Windows" else "ping -c 4 8.8.8.8")
    ejecutar("nslookup google.com")

# GUARDAR REPORTE
def guardar_reporte():
    txt = salida.get(1.0, tk.END).strip()
    if not txt:
        messagebox.showwarning("Aviso", "No hay nada para guardar.")
        return
    nombre = f"reporte_red_{datetime.datetime.now():%Y%m%d_%H%M}.txt"
    with open(nombre, "w", encoding="utf-8") as f:
        f.write(txt)
    messagebox.showinfo("OK", f"Reporte guardado:\n{nombre}")

# ----------------------------------------------------------
# DEFINICIÓN DE CATEGORÍAS (MAGIA SIMPLE)
# ----------------------------------------------------------
CATEGORIAS = {
    "Diagnóstico de red": {
        "info": "Comandos clásicos para analizar conectividad y estado de red.\nNo modifican el sistema.",
        "acciones": [
            ("Ver IP", ver_ip),
            ("IP Detallada", ip_detallada),
            ("Ping", ping),
            ("Traceroute", traceroute),
            ("PathPing / MTR", pathping),
            ("NSLookup", nslookup),
            ("Conexiones", conexiones)
        ]
    },
    "ARP": {
        "info": "ARP gestiona la relación IP ↔ MAC.\n\nBorrar la caché puede interrumpir conexiones.",
        "acciones": [
            ("Listar caché ARP", arp_listar),
            ("Borrar caché ARP", arp_borrar)
        ]
    },
    "Servicios": {
        "info": "Permite listar, iniciar o detener servicios del sistema.\n\n⚠ Usar con conocimiento.",
        "acciones": [
            ("Listar servicios", servicios_listar),
            ("Iniciar servicio", servicio_iniciar),
            ("Detener servicio", servicio_detener)
        ]
    },
    "Sistema": {
        "info": "Información básica del sistema y red.\n\nAlgunos comandos solo existen en Windows.",
        "acciones": [
            ("Hostname", hostname_cmd),
            ("Direcciones MAC", mac)
        ]
    }
}

# ----------------------------------------------------------
# GUI
# ----------------------------------------------------------
root = tk.Tk()
root.title("Red Tools")
root.geometry("1150x720")
root.configure(bg="#020617")

# HEADER
header = tk.Label(
    root,
    text=f"Red Tools – Sistema detectado: {OS}",
    bg="#020617",
    fg="#22d3ee",
    font=("Arial", 14, "bold")
)
header.pack(fill=tk.X, pady=6)

# CUERPO SUPERIOR (3 COLUMNAS)
top = tk.Frame(root, bg="#020617")
top.pack(fill=tk.X, padx=8)

# Columna 1: menú
menu = tk.Frame(top, bg="#020617", width=220)
menu.pack(side=tk.LEFT, fill=tk.Y, padx=6)

# Columna 2: acciones
acciones = tk.Frame(top, bg="#020617")
acciones.pack(side=tk.LEFT, fill=tk.Y, padx=6)

# Columna 3: info
info = tk.Frame(top, bg="#0f172a", width=350)
info.pack(side=tk.LEFT, fill=tk.Y, padx=6)
info.pack_propagate(False)

info_label = tk.Label(
    info,
    text="Seleccione una categoría del menú.",
    bg="#0f172a",
    fg="#cbd5f5",
    justify="left",
    wraplength=330
)
info_label.pack(anchor="w", padx=8, pady=8)

# ----------------------------------------------------------
# FUNCIÓN PARA CAMBIAR CATEGORÍA
# ----------------------------------------------------------
def mostrar_categoria(nombre):
    # Limpiar botones viejos
    for w in acciones.winfo_children():
        w.destroy()

    info_label.config(text=CATEGORIAS[nombre]["info"])

    for texto, funcion in CATEGORIAS[nombre]["acciones"]:
        tk.Button(
            acciones,
            text=texto,
            width=32,
            bg="#1e293b",
            fg="white",
            command=funcion
        ).pack(pady=2)

# Botones de menú
for cat in CATEGORIAS:
    tk.Button(
        menu,
        text=cat,
        width=22,
        bg="#334155",
        fg="white",
        command=lambda c=cat: mostrar_categoria(c)
    ).pack(pady=3)

# Botones inferiores del menú
tk.Button(menu, text="Diagnóstico Internet", width=22,
          bg="#14532d", fg="white",
          command=diagnostico_internet).pack(pady=6)

tk.Button(menu, text="Guardar Reporte", width=22,
          bg="#1d4ed8", fg="white",
          command=guardar_reporte).pack(pady=3)

tk.Button(menu, text="SALIR", width=22,
          bg="#7f1d1d", fg="white",
          command=root.quit).pack(pady=12)

# ----------------------------------------------------------
# SALIDA DE COMANDOS
# ----------------------------------------------------------
salida = scrolledtext.ScrolledText(
    root,
    bg="#020617",
    fg="#22c55e",
    font=("Consolas", 10)
)
salida.pack(expand=True, fill=tk.BOTH, padx=8, pady=8)

root.mainloop()
