# Guía Completa: Comunicación entre Servidores y Consumo de APIs

## Preparación Inicial

### Requisitos Previos
- Dos máquinas virtuales con Ubuntu Server
- Acceso SSH a ambas máquinas
- Conexión de red entre las máquinas

### Identificación de las Máquinas
Primero, identifica las IPs de tus máquinas:

**En cada máquina ejecuta:**
```bash
ip addr show
# o también
hostname -I
```

Anota las IPs:
- Máquina 1 (Servidor): `___.___.___.__`
- Máquina 2 (Cliente): `___.___.___.__`

## Módulo 1: Preparación de los Servidores

### 1.1 Verificación de Conectividad

**Desde Máquina 1 hacia Máquina 2:**
```bash
ping <IP_de_maquina_2>
```

**Desde Máquina 2 hacia Máquina 1:**
```bash
ping <IP_de_maquina_1>
```

Si el ping funciona, presiona `Ctrl+C` para detenerlo. Si no funciona, verifica la configuración de red.

### 1.2 Configuración del Servidor (Máquina 1)

#### Instalación de Dependencias
```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install Flask
```

#### Crear el Archivo del Servidor
```bash
nano app.py
```

Copia este contenido en el archivo:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/saludo')
def saludo():
    return jsonify(mensaje="Hola desde el servidor!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Guarda el archivo: `Ctrl+O`, luego `Enter`, luego `Ctrl+X`

### 1.3 Configuración del Firewall
```bash
sudo ufw allow 5000/tcp
```

### 1.4 Ejecutar el Servidor
```bash
python3 app.py
```

Deberías ver un mensaje como: `Running on http://0.0.0.0:5000`

**Nota:** Deja esta terminal abierta con el servidor ejecutándose.

## Módulo 2: Consumo del Servicio (Máquina 2)

### 2.1 Prueba Básica con curl

**Desde una nueva terminal en Máquina 2:**
```bash
curl http://<IP_del_servidor>:5000/saludo
```

**Respuesta esperada:**
```json
{"mensaje":"Hola desde el servidor!"}
```

### Resolución de Problemas Comunes

Si no funciona, verifica:

1. **El servidor está ejecutándose en Máquina 1**
2. **El firewall permite el tráfico:**
   ```bash
   sudo ufw status
   ```
3. **La conectividad de red:**
   ```bash
   telnet <IP_del_servidor> 5000
   ```

## Módulo 3: Intercambio de Datos y Autenticación

### 3.1 Actualización del Servidor (Máquina 1)

**Detén el servidor anterior:** `Ctrl+C`

**Actualiza el archivo app.py:**
```bash
nano app.py
```

Reemplaza el contenido con:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/saludo/<nombre>')
def saludo_personalizado(nombre):
    return jsonify(mensaje=f"Hola, {nombre}! Has consumido el servicio.")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    clave = data.get('clave')
    if usuario == 'admin' and clave == '1234':
        return jsonify(mensaje="Autenticación exitosa"), 200
    else:
        return jsonify(mensaje="Credenciales inválidas"), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Ejecuta el servidor actualizado:**
```bash
python3 app.py
```

### 3.2 Pruebas Avanzadas (Máquina 2)

#### Prueba con Parámetros
```bash
curl http://<IP_del_servidor>:5000/saludo/Ana
```

**Respuesta esperada:**
```json
{"mensaje":"Hola, Ana! Has consumido el servicio."}
```

#### Prueba de Autenticación Exitosa
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"usuario":"admin","clave":"1234"}' \
     http://<IP_del_servidor>:5000/login
```

**Respuesta esperada:**
```json
{"mensaje":"Autenticación exitosa"}
```

#### Prueba de Autenticación Fallida
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"usuario":"admin","clave":"wrong"}' \
     http://<IP_del_servidor>:5000/login
```

**Respuesta esperada:**
```json
{"mensaje":"Credenciales inválidas"}
```

## Verificación Final

### Checklist de Completitud

- [ ] Ping funciona entre ambas máquinas
- [ ] Flask instalado en Máquina 1
- [ ] Puerto 5000 abierto en firewall
- [ ] Servidor ejecutándose correctamente
- [ ] Endpoint `/saludo` funcional
- [ ] Endpoint `/saludo/<nombre>` funcional
- [ ] Endpoint `/login` funcional con autenticación

### Comandos Útiles para Depuración

**Ver procesos usando el puerto 5000:**
```bash
sudo netstat -tlnp | grep 5000
```

**Ver logs del firewall:**
```bash
sudo ufw status verbose
```

**Probar conectividad específica:**
```bash
nc -zv <IP_del_servidor> 5000
```

## Extensiones Opcionales

### Agregar Más Endpoints

Puedes expandir tu API agregando más funcionalidades al archivo `app.py`:

```python
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "servidor": "Mi API Python",
        "version": "1.0",
        "endpoints": ["/saludo", "/saludo/<nombre>", "/login", "/info"]
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify(status="OK", timestamp=str(datetime.now()))
```

### Usar un Cliente Python

Crea un archivo `cliente.py` en Máquina 2:

```python
import requests
import json

# Configuración
SERVER_IP = "<IP_del_servidor>"
BASE_URL = f"http://{SERVER_IP}:5000"

# Prueba básica
response = requests.get(f"{BASE_URL}/saludo/PythonClient")
print("Respuesta del saludo:", response.json())

# Prueba de autenticación
auth_data = {"usuario": "admin", "clave": "1234"}
response = requests.post(f"{BASE_URL}/login", json=auth_data)
print("Respuesta del login:", response.json())
```

powershell
# Eliminar permisos heredados
icacls "C:\ssh_keys\breiner.pem" /inheritance:r

# Dar permiso solo de lectura al usuario actual
icacls "C:\ssh_keys\breiner.pem" /grant:r "desktop-3h0ku6i\usuario:R"

# Eliminar permisos de otros grupos (si aparecen)
icacls "C:\ssh_keys\breiner.pem" /remove "NT AUTHORITY\Usuarios autentificados"


