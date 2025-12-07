#!/usr/bin/env python3
# ==========================================================
# red-tools.py
# Herramienta de Diagnóstico de Red - Multiplataforma
#
# Sistemas soportados:
#   - Windows
#   - Linux
#
# Funcionalidades:
#   - Comandos clásicos de red (ipconfig, ping, tracert, etc.)
#   - Diagnóstico automático de Internet
#   - Diagnóstico completo en 1 click
#   - Manejo de caché ARP (listar / borrar)
#   - Gestión básica de servicios (start / stop)
#   - Pathping / MTR (ruta + pérdida de paquetes)
#   - Guardado de reportes (.txt)
#
# Autor: Tino
# ==========================================================

import platform
import subprocess
import datetime
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

# ----------------------------------------------------------
# DETECCIÓN DEL SISTEMA OPERATIVO
# ----------------------------------------------------------
OS = platform.system()  # Windows | Linux

# ----------------------------------------------------------
# FUNCIÓN CENTRAL: EJECUTAR COMANDOS
# ----------------------------------------------------------
def ejecutar(comando):
    output.insert(tk.END, f"\n> {comando}\n")
    try:
        resultado = subprocess.check_output(
            comando,
            shell=True,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="cp850" if OS == "Windows" else "utf-8",
            errors="replace"
        )
        output.insert(tk.END, resultado)
    except subprocess.CalledProcessError as e:
        output.insert(tk.END, e.output)

    output.see(tk.END)


# ----------------------------------------------------------
# COMANDOS DE RED BÁSICOS
# ----------------------------------------------------------
def ver_ip():
    ejecutar("ipconfig" if OS == "Windows" else "ip a")

def ip_detallada():
    ejecutar("ipconfig /all" if OS == "Windows" else "ip a && ip r")

def liberar_ip():
    ejecutar("ipconfig /release" if OS == "Windows" else "sudo dhclient -r")

def renovar_ip():
    ejecutar("ipconfig /renew" if OS == "Windows" else "sudo dhclient")

def flush_dns():
    ejecutar(
        "ipconfig /flushdns"
        if OS == "Windows"
        else "sudo systemd-resolve --flush-caches"
    )

def ping():
    host = simpledialog.askstring("Ping", "IP o dominio:")
    if host:
        ejecutar(f"ping {host}" if OS == "Windows" else f"ping -c 4 {host}")

def traceroute():
    host = simpledialog.askstring("Traceroute", "IP o dominio:")
    if host:
        ejecutar("tracert " + host if OS == "Windows" else "traceroute " + host)

def nslookup():
    dom = simpledialog.askstring("NSLookup", "Dominio:")
    if dom:
        ejecutar("nslookup " + dom)

def conexiones():
    ejecutar("netstat -an" if OS == "Windows" else "ss -tulpn")

def hostname_cmd():
    ejecutar("hostname")

def mac():
    ejecutar("getmac" if OS == "Windows" else "ip link")

# ----------------------------------------------------------
# ARP
# ----------------------------------------------------------
def arp_listar():
    ejecutar("arp -a" if OS == "Windows" else "ip neigh")

def arp_borrar():
    if not messagebox.askyesno(
        "ADVERTENCIA",
        "Esto borrará la caché ARP.\n"
        "Puede afectar conexiones activas.\n\n"
        "¿Desea continuar?"
    ):
        return

    ejecutar("arp -d *" if OS == "Windows" else "sudo ip neigh flush all")

# ----------------------------------------------------------
# PATHPING / MTR
# ----------------------------------------------------------
def pathping():
    host = simpledialog.askstring("PathPing / MTR", "IP o dominio:")
    if not host:
        return

    if OS == "Windows":
        ejecutar("pathping " + host)
    else:
        ejecutar("mtr -r " + host)

# ----------------------------------------------------------
# SERVICIOS (START / STOP)
# ----------------------------------------------------------
def servicios_listar():
    ejecutar("net start" if OS == "Windows" else "systemctl list-units --type=service")

def servicio_iniciar():
    servicio = simpledialog.askstring("Iniciar servicio", "Nombre del servicio:")
    if servicio:
        ejecutar(
            f"net start {servicio}"
            if OS == "Windows"
            else f"sudo systemctl start {servicio}"
        )

def servicio_detener():
    servicio = simpledialog.askstring("Detener servicio", "Nombre del servicio:")
    if servicio:
        ejecutar(
            f"net stop {servicio}"
            if OS == "Windows"
            else f"sudo systemctl stop {servicio}"
        )

# ----------------------------------------------------------
# DIAGNÓSTICO INTERNET
# ----------------------------------------------------------
def diagnostico_internet():
    output.delete(1.0, tk.END)
    output.insert(tk.END, "🌐 DIAGNÓSTICO DE INTERNET\n")
    output.insert(tk.END, "=" * 40 + "\n")

    cmds = [
        "ipconfig" if OS == "Windows" else "ip a",
        "ping 8.8.8.8" if OS == "Windows" else "ping -c 4 8.8.8.8",
        "nslookup google.com"
    ]

    for c in cmds:
        ejecutar(c)

# ----------------------------------------------------------
# DIAGNÓSTICO COMPLETO
# ----------------------------------------------------------
def diagnostico_completo():
    output.delete(1.0, tk.END)
    output.insert(tk.END, "🚀 DIAGNÓSTICO COMPLETO DE RED\n")
    output.insert(tk.END, "=" * 50 + "\n")

    acciones = [
        ("Información IP", ver_ip),
        ("IP detallada", ip_detallada),
        ("Conexiones activas", conexiones),
        ("ARP", arp_listar),
        ("Hostname", hostname_cmd),
        ("MAC", mac),
    ]

    for titulo, func in acciones:
        output.insert(tk.END, f"\n--- {titulo} ---\n")
        func()

# ----------------------------------------------------------
# GUARDAR REPORTE
# ----------------------------------------------------------
def guardar_reporte():
    texto = output.get(1.0, tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "No hay datos para guardar.")
        return

    fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    archivo = f"reporte_red_{fecha}.txt"

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(texto)

    messagebox.showinfo("Reporte guardado", f"Archivo creado:\n{archivo}")

# ==========================================================
# INTERFAZ GRÁFICA
# ==========================================================
root = tk.Tk()
root.title(f"Red Tools - {OS}")
root.geometry("960x620")
root.configure(bg="#020617")

frame = tk.Frame(root, bg="#020617")
frame.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)

btn_cfg = {"width": 32, "bg": "#1e293b", "fg": "white", "pady": 3}

tk.Label(
    frame,
    text=f"SISTEMA: {OS}",
    font=("Arial", 12, "bold"),
    fg="#22d3ee",
    bg="#020617"
).pack(pady=8)

# Botones básicos
tk.Button(frame, text="Ver IP", command=ver_ip, **btn_cfg).pack()
tk.Button(frame, text="IP detallada", command=ip_detallada, **btn_cfg).pack()
tk.Button(frame, text="Liberar IP", command=liberar_ip, **btn_cfg).pack()
tk.Button(frame, text="Renovar IP", command=renovar_ip, **btn_cfg).pack()
tk.Button(frame, text="Vaciar DNS", command=flush_dns, **btn_cfg).pack()
tk.Button(frame, text="Ping", command=ping, **btn_cfg).pack()
tk.Button(frame, text="Traceroute", command=traceroute, **btn_cfg).pack()
tk.Button(frame, text="PathPing / MTR", command=pathping, **btn_cfg).pack()
tk.Button(frame, text="NSLookup", command=nslookup, **btn_cfg).pack()
tk.Button(frame, text="Conexiones", command=conexiones, **btn_cfg).pack()

# ARP
tk.Button(frame, text="ARP - Listar", command=arp_listar, **btn_cfg).pack(pady=4)
tk.Button(frame, text="ARP - Borrar caché", bg="#7c2d12",
          fg="white", width=32, command=arp_borrar).pack()

# Servicios
tk.Button(frame, text="Servicios - Listar", command=servicios_listar, **btn_cfg).pack(pady=4)
tk.Button(frame, text="Servicios - Iniciar", command=servicio_iniciar, **btn_cfg).pack()
tk.Button(frame, text="Servicios - Detener", command=servicio_detener, **btn_cfg).pack()

# Diagnóstico
tk.Button(frame, text="🌐 Diagnóstico Internet",
          bg="#14532d", fg="white", width=32,
          command=diagnostico_internet).pack(pady=6)

tk.Button(frame, text="🚀 Diagnóstico Completo",
          bg="#0f766e", fg="white", width=32,
          command=diagnostico_completo).pack()

tk.Button(frame, text="💾 Guardar Reporte",
          bg="#1d4ed8", fg="white", width=32,
          command=guardar_reporte).pack(pady=6)

tk.Button(frame, text="Salir",
          bg="#7f1d1d", fg="white", width=32,
          command=root.quit).pack(pady=10)

# Salida
output = scrolledtext.ScrolledText(
    root, bg="#020617", fg="#22c55e",
    font=("Consolas", 10), wrap=tk.WORD
)
output.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=6, pady=6)

root.mainloop()
