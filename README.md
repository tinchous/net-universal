# 🖧 Red Tools
### Herramienta de Diagnóstico de Red – Multiplataforma (Windows / Linux)

**Red Tools** es una aplicación gráfica desarrollada en Python para realizar
diagnósticos de red, análisis de conectividad y tareas básicas de administración
en sistemas **Windows y Linux**, desde una única interfaz amigable.

Está pensada tanto para **uso técnico real** como **uso educativo**
(estudiantes, docentes, cursos de redes).

---

## 🚀 Características principales

✅ Interfaz gráfica (Tkinter)
✅ Multiplataforma: Windows / Linux
✅ Detección automática del sistema operativo
✅ Comandos clásicos de red
✅ Diagnóstico automático de Internet
✅ Diagnóstico completo en 1 click
✅ Manejo de caché ARP
✅ Gestión básica de servicios
✅ PathPing / MTR (ruta + pérdida de paquetes)
✅ Guardado de reportes en `.txt`
✅ Manejo correcto de encoding en Windows

---

## 🧠 Comandos disponibles

### Diagnóstico de red
- `ipconfig` / `ip a`
- `ipconfig /all`
- `ping`
- `tracert` / `traceroute`
- `pathping` (Windows) / `mtr` (Linux)
- `nslookup`
- `netstat -an` / `ss`

### ARP
- Listar caché ARP (`arp -a`)
- Borrar caché ARP (`arp -d` / `ip neigh flush`)

### Servicios
- Listar servicios (`net start` / `systemctl`)
- Iniciar servicios (`net start <servicio>`)
- Detener servicios (`net stop <servicio>`)

### Sistema
- Hostname
- Direcciones MAC
- Comandos avanzados (`netsh`, Windows)

---

## 🌐 Diagnóstico automático de Internet

La opción **“Diagnóstico Internet”** verifica:

1. Configuración IP
2. Conectividad con Internet (ping a 8.8.8.8)
3. Resolución DNS

Ideal para detectar problemas básicos rápidamente.

---

## 🚀 Diagnóstico completo (1 click)

Ejecuta en orden:

- Información IP
- IP detallada
- Conexiones activas
- Caché ARP
- Hostname
- MAC addresses

Pensado para:
- Soporte técnico
- Auditoría básica
- Clases y demostraciones

---

## 💾 Guardado de reportes

Permite guardar **todo el resultado mostrado** en un archivo de texto:
reporte_red_YYYY-MM-DD_HH-MM.txt


Útil para:
- Enviar a soporte
- Documentar fallos
- Uso educativo
- Portfolio

---

## 🖥️ Requisitos

### Windows
- Windows 10 / 11
- Python **3.10 o superior**
- Recomendado: ejecutar como **Administrador**

### Linux
- Python 3
- Herramientas comunes instaladas (`ip`, `ping`, `traceroute`, `mtr`)
- Algunos comandos requieren `sudo`

---

## ▶️ Instalación y ejecución

Clonar el repositorio:
```bash
git clone https://github.com/tuusuario/net-universal.git
cd net-universal
ejecutar en linux :
python3 red-tools.py
o en windows :
py red-tools.py
