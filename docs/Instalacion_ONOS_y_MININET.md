@@ -1,21 +1,33 @@

# 🌐 **Guía completa: ONOS + Mininet en Ubuntu**

## **1. Actualizar el sistema**
---

## **1. Requisitos previos**

Antes de comenzar, asegúrate de tener:

* **VirtualBox** instalado.
* Ubuntu 20.04 o 22.04 como sistema operativo en la máquina virtual.
* Al menos **4 GB de RAM** y **2 CPUs** asignadas a la VM.
* Conexión a internet estable.

Antes de instalar cualquier cosa:
---

## **2. Actualizar Ubuntu**

Antes de instalar cualquier cosa, actualiza tus paquetes:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git curl wget unzip -y
sudo apt install git curl wget unzip net-tools -y
```

---

## **2. Instalar Mininet**

Mininet es bastante sencillo de instalar.
## **3. Instalar Mininet**

### **Instalación automática**
Mininet es el emulador que simulará la red SDN.

```bash
git clone https://github.com/mininet/mininet.git
@ -23,156 +35,302 @@ cd mininet
sudo ./util/install.sh -a
```

* El parámetro `-a` instala **todas las dependencias** (Open vSwitch, controladores, etc.).
> `-a` instala **todas las dependencias**: Open vSwitch, controladores, etc.

### **Verificar instalación**
### **Verificar instalación:**

```bash
sudo mn --test pingall
```

Si ves que los hosts se hacen *ping* correctamente, **Mininet está listo** .
Si todo funciona, verás que los hosts se hacen *ping* entre sí ✅.

---

## **3. Instalar Java 17 (requerido por ONOS)**
## **4. Instalar Docker (para ejecutar ONOS fácilmente)**

ONOS necesita **Java 11 o superior**. Recomiendo **Java 17**.
ONOS se ejecutará dentro de un contenedor Docker.

```bash
sudo apt install openjdk-17-jdk -y
sudo apt install docker.io docker-compose -y
```

Verifica la instalación:
Habilitar Docker para que inicie automáticamente:

```bash
java -version
sudo systemctl enable docker --now
```

Debe aparecer algo como:
Agregar tu usuario al grupo `docker`:

```bash
sudo usermod -aG docker $USER
```

> **IMPORTANTE:** Cierra sesión o reinicia la máquina virtual para que los cambios se apliquen:

```bash
reboot
```
openjdk version "17.0.x"

Verifica que Docker funciona sin `sudo`:

```bash
docker ps
```

---

## **4. Instalar ONOS**
## **5. Descargar y ejecutar ONOS**

ONOS tiene varias formas de instalación. Vamos a hacerlo con **Docker** (más fácil) y **sin Docker** (opcional).
ONOS es el controlador SDN que administrará los switches virtuales de Mininet.

### **Opción A: Instalar ONOS usando Docker (recomendado)**
```bash
docker pull onosproject/onos
```

1. **Instalar Docker**:
Ejecuta ONOS:

   ```bash
   sudo apt install docker.io docker-compose -y
   sudo systemctl enable docker --now
   sudo usermod -aG docker $USER
   ```
```bash
docker run -d --name onos -p 8181:8181 -p 8101:8101 -p 6653:6653 onosproject/onos
```

   >  ! Cierra y vuelve a abrir la sesión para aplicar el cambio de grupo.
* **8181:** interfaz web (GUI).
* **8101:** consola administrativa.
* **6653:** puerto OpenFlow para Mininet.

2. **Descargar imagen de ONOS**:
---

   ```bash
   docker pull onosproject/onos
   ```
## **6. Confirmar que ONOS está corriendo**

3. **Ejecutar ONOS**:
```bash
docker ps
```

   ```bash
   docker run -d --name onos -p 8181:8181 -p 8101:8101 -p 6653:6653 onosproject/onos
   ```
Debes ver algo como:

   * **8181** → Interfaz web (GUI)
   * **8101** → Consola de administración (SSH)
   * **6653** → Puerto OpenFlow (conexión con Mininet)
```
CONTAINER ID   IMAGE              STATUS          PORTS
abcd1234efgh   onosproject/onos   Up 30 seconds   0.0.0.0:6653->6653/tcp, 0.0.0.0:8181->8181/tcp
```

4. **Acceder a la interfaz web**
   En tu navegador, ve a:
Si necesitas ver logs en tiempo real:

   ```
   http://<IP_DE_UBUNTU>:8181/onos/ui
   ```
```bash
docker logs -f onos
```

---

   Usuario y contraseña por defecto:
## **7. Configurar VirtualBox para acceso externo**

   ```
   admin / rocks
   ```
Actualmente tu VM tiene una IP como `10.0.2.x` (modo NAT), que **no permite conexiones externas**.

### **Pasos:**

1. **Apaga tu máquina virtual.**
2. En VirtualBox → **Configuración → Red → Adaptador 1**:

   * **Habilitar adaptador de red** ✅
   * **Conectado a:** `Adaptador puente` (*Bridged Adapter*)
   * **Nombre:** selecciona tu tarjeta de red física (WiFi o Ethernet).
3. Guarda y enciende la VM nuevamente.

---

### **Opción B: Instalar ONOS sin Docker (manual)**
## **8. Obtener la nueva IP de Ubuntu**

1. Instala dependencias:
```bash
ip a
```

   ```bash
   sudo apt install maven zip -y
   ```
Debes ver una IP tipo `192.168.x.x` o `172.16.x.x`.
Ejemplo:

2. Descarga ONOS:
```
inet 192.168.1.105/24
```

   ```bash
   git clone https://github.com/opennetworkinglab/onos.git
   cd onos
   ```
Esta será la IP que usarás para:

3. Compila y ejecuta:
* Acceder a la GUI de ONOS.
* Conectar Mininet con el controlador.

   ```bash
   tools/build/onos-buck build onos
   tools/build/onos-buck run onos-local
   ```
---

## **9. Acceder a la interfaz web de ONOS**

Esto tardará un poco, pero luego ONOS estará disponible en `http://localhost:8181/onos/ui`.
Desde tu PC **host**, abre el navegador y ve a:

```
http://192.168.1.105:8181/onos/ui
```

> Cambia `192.168.1.105` por la IP de tu VM.

**Credenciales por defecto:**

```
Usuario: admin
Contraseña: rocks
```

---

## **5. Conectar Mininet con ONOS**
## **10. Conectar Mininet a ONOS**

1. Inicia Mininet con un switch OpenFlow:
Ahora que ONOS está corriendo, inicia Mininet con un switch OpenFlow controlado por ONOS:

   ```bash
   sudo mn --topo tree,2 --controller=remote,ip=<IP_DE_UBUNTU>,port=6653 --switch ovs,protocols=OpenFlow13
   ```
```bash
sudo mn --topo tree,2 --controller=remote,ip=192.168.1.105,port=6653 --switch ovs,protocols=OpenFlow13
```

* `--topo tree,2` → crea una topología en forma de árbol de dos niveles.
* `--controller=remote` → usa ONOS como controlador remoto.
* `--switch ovs,protocols=OpenFlow13` → asegura compatibilidad con OpenFlow 1.3.

   * Cambia `<IP_DE_UBUNTU>` por la IP de tu máquina virtual.
     Puedes verla con:
---

     ```bash
     ip a
     ```
## **11. Verificar la conexión en ONOS**

2. Verifica en ONOS:
En la GUI de ONOS:

   * Ve a **ONOS GUI → Devices**, y deberías ver los switches conectados.
* Ve a **Topology → Devices** → deben aparecer los switches (`s1`, `s2`, `s3`).
* Ve a **Hosts** → deben aparecer los hosts (`h1`, `h2`, etc.).

---

## **6. Probar la conexión**
## **12. Probar la red desde Mininet**

Dentro de Mininet:
En la terminal de Mininet:

```bash
pingall
```

Si ONOS está controlando la red, verás que los paquetes se enrutan correctamente.
Si todo funciona correctamente, verás algo como:

```
h1 -> h2 h3 h4
h2 -> h1 h3 h4
h3 -> h1 h2 h4
h4 -> h1 h2 h3
*** Results: 0% dropped (12/12 received)
```

Esto confirma que **ONOS está gestionando la red SDN** ✅.

---

## **7. Tips importantes**
## **13. Solución de problemas**

### **a) Mininet no detecta ONOS**

Error:

```
Unable to contact the remote controller at 192.168.1.105:6653
```

* Si usas **VirtualBox**, configura el adaptador de red en **Modo Puente** para poder acceder a ONOS desde tu PC anfitrión.
* Usuario y contraseña por defecto de ONOS:
Solución:

* Verifica que ONOS está activo:

  ```bash
  docker ps
  ```
  admin / rocks
* Comprueba que el puerto 6653 está escuchando:

  ```bash
  netstat -tulnp | grep 6653
  ```
* Para ver logs en tiempo real:
* Si no aparece, reinicia ONOS:

  ```bash
  docker logs -f onos
  docker restart onos
  ```

---

### **b) Firewall bloqueando puertos**

Si ONOS está corriendo pero Mininet no se conecta:

```bash
sudo ufw allow 6653
sudo ufw allow 8181
sudo ufw status
```

---

### **c) Logs en tiempo real**

Para ver los eventos de ONOS:

```bash
docker logs -f onos
```

---

## **14. Arquitectura final**

```
+-------------------+        +---------------------------+
|      Host PC       |        |      Máquina Virtual      |
| Navegador Web      |        | Ubuntu + Docker + ONOS    |
| http://192.168.1.105:8181  |        | Mininet (OVS)             |
+-------------------+        +---------------------------+
                                      |
                                      | OpenFlow (puerto 6653)
                                      |
                                [Switches virtuales]
                                 /           \
                               h1             h2
```

---

## **15. Comandos útiles**

| Acción                         | Comando               |
| ------------------------------ | --------------------- |
| Listar contenedores activos    | `docker ps`           |
| Detener ONOS                   | `docker stop onos`    |
| Iniciar ONOS                   | `docker start onos`   |
| Ver logs de ONOS               | `docker logs -f onos` |
| Salir de Mininet               | `exit`                |
| Probar conectividad en Mininet | `pingall`             |

---

## **16. Flujo final de ejecución**

1. Arranca ONOS:

   ```bash
   docker start onos
   ```
2. Verifica IP de Ubuntu:

   ```bash
   ip a
   ```
3. Conecta Mininet a ONOS:

   ```bash
   sudo mn --topo tree,2 --controller=remote,ip=<IP_UBUNTU>,port=6653 --switch ovs,protocols=OpenFlow13
   ```
4. Abre la GUI en el navegador:

   ```
   http://<IP_UBUNTU>:8181/onos/ui
   ```
5. Realiza pruebas:

   ```bash
   pingall
   ```

