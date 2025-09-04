

## **1. Actualizar el sistema**

Antes de instalar cualquier cosa:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git curl wget unzip -y
```

---

## **2. Instalar Mininet**

Mininet es bastante sencillo de instalar.

### **Instalación automática**

```bash
git clone https://github.com/mininet/mininet.git
cd mininet
sudo ./util/install.sh -a
```

* El parámetro `-a` instala **todas las dependencias** (Open vSwitch, controladores, etc.).

### **Verificar instalación**

```bash
sudo mn --test pingall
```

Si ves que los hosts se hacen *ping* correctamente, **Mininet está listo** .

---

## **3. Instalar Java 17 (requerido por ONOS)**

ONOS necesita **Java 11 o superior**. Recomiendo **Java 17**.

```bash
sudo apt install openjdk-17-jdk -y
```

Verifica la instalación:

```bash
java -version
```

Debe aparecer algo como:

```
openjdk version "17.0.x"
```

---

## **4. Instalar ONOS**

ONOS tiene varias formas de instalación. Vamos a hacerlo con **Docker** (más fácil) y **sin Docker** (opcional).

### **Opción A: Instalar ONOS usando Docker (recomendado)**

1. **Instalar Docker**:

   ```bash
   sudo apt install docker.io docker-compose -y
   sudo systemctl enable docker --now
   sudo usermod -aG docker $USER
   ```

   >  ! Cierra y vuelve a abrir la sesión para aplicar el cambio de grupo.

2. **Descargar imagen de ONOS**:

   ```bash
   docker pull onosproject/onos
   ```

3. **Ejecutar ONOS**:

   ```bash
   docker run -d --name onos -p 8181:8181 -p 8101:8101 -p 6653:6653 onosproject/onos
   ```

   * **8181** → Interfaz web (GUI)
   * **8101** → Consola de administración (SSH)
   * **6653** → Puerto OpenFlow (conexión con Mininet)

4. **Acceder a la interfaz web**
   En tu navegador, ve a:

   ```
   http://<IP_DE_UBUNTU>:8181/onos/ui
   ```

   Usuario y contraseña por defecto:

   ```
   admin / rocks
   ```

---

### **Opción B: Instalar ONOS sin Docker (manual)**

1. Instala dependencias:

   ```bash
   sudo apt install maven zip -y
   ```

2. Descarga ONOS:

   ```bash
   git clone https://github.com/opennetworkinglab/onos.git
   cd onos
   ```

3. Compila y ejecuta:

   ```bash
   tools/build/onos-buck build onos
   tools/build/onos-buck run onos-local
   ```

Esto tardará un poco, pero luego ONOS estará disponible en `http://localhost:8181/onos/ui`.

---

## **5. Conectar Mininet con ONOS**

1. Inicia Mininet con un switch OpenFlow:

   ```bash
   sudo mn --topo tree,2 --controller=remote,ip=<IP_DE_UBUNTU>,port=6653 --switch ovs,protocols=OpenFlow13
   ```

   * Cambia `<IP_DE_UBUNTU>` por la IP de tu máquina virtual.
     Puedes verla con:

     ```bash
     ip a
     ```

2. Verifica en ONOS:

   * Ve a **ONOS GUI → Devices**, y deberías ver los switches conectados.

---

## **6. Probar la conexión**

Dentro de Mininet:

```bash
pingall
```

Si ONOS está controlando la red, verás que los paquetes se enrutan correctamente.

---

## **7. Tips importantes**

* Si usas **VirtualBox**, configura el adaptador de red en **Modo Puente** para poder acceder a ONOS desde tu PC anfitrión.
* Usuario y contraseña por defecto de ONOS:

  ```
  admin / rocks
  ```
* Para ver logs en tiempo real:

  ```bash
  docker logs -f onos
  ```
