Para eliminar **todo lo que has instalado** (Mininet, ONOS en Docker, redes de Docker, etc.) y dejar tu sistema limpio, sigue estos pasos:

---

## **1. Eliminar la topología de Mininet**

Antes de desinstalar, asegúrate de limpiar procesos activos de Mininet y Open vSwitch:

```bash
sudo mn -c
```

Esto elimina redes, switches virtuales y procesos que quedaron en memoria.

---

## **2. Desinstalar Mininet**

Si instalaste Mininet desde el repositorio de GitHub:

```bash
cd ~/mininet
sudo make uninstall
```

> Si no recuerdas en qué carpeta está Mininet, usa:
>
> ```bash
> cd ~
> ls
> ```
>
> Busca la carpeta llamada `mininet`.

Luego borra la carpeta:

```bash
cd ~
rm -rf mininet
```

---

## **3. Eliminar ONOS en Docker**

### **a) Listar contenedores**

```bash
docker ps -a
```

Verás algo como:

```
CONTAINER ID   IMAGE              STATUS          NAMES
abcd1234efgh   onosproject/onos   Exited (0)      onos
```

---

### **b) Detener y eliminar contenedor**

```bash
docker stop onos
docker rm onos
```

---

### **c) Eliminar la imagen de ONOS**

```bash
docker images
```

Salida esperada:

```
REPOSITORY          TAG       IMAGE ID       CREATED        SIZE
onosproject/onos    latest    4fbb2fbaec72   2 days ago     470MB
```

Borra la imagen:

```bash
docker rmi onosproject/onos
```

---

## **4. Eliminar redes de Docker creadas automáticamente**

```bash
docker network prune
```

> Escribe `y` cuando te pida confirmación.

Esto limpia redes virtuales viejas creadas por Docker.

---

## **5. Desinstalar Docker (opcional)**

Si deseas eliminar Docker completamente:

```bash
sudo apt-get purge docker.io docker-compose docker-doc docker-ce docker-ce-cli
sudo apt-get autoremove --purge -y
sudo rm -rf /var/lib/docker
```

Verifica que ya no esté instalado:

```bash
docker --version
```

Debe decir `command not found`.

---

## **6. Limpiar Open vSwitch**

Open vSwitch viene con Mininet y puede dejar servicios activos.

```bash
sudo systemctl stop openvswitch-switch
sudo systemctl disable openvswitch-switch
sudo apt-get purge openvswitch-switch -y
```

Verifica que no haya interfaces virtuales:

```bash
ip a
```

No deberías ver interfaces como `s1`, `s2`, `s3` o `ovs-system`.

---

## **7. Limpiar dependencias sobrantes**

```bash
sudo apt autoremove -y
sudo apt autoclean
```

---

## **8. Confirmar limpieza final**

* **Mininet:**

  ```bash
  which mn
  ```

  → No debe devolver ninguna ruta.

* **ONOS:**

  ```bash
  docker ps -a
  ```

  → No debe mostrar ningún contenedor.

* **Open vSwitch:**

  ```bash
  ovs-vsctl show
  ```

  → Debe decir `command not found`.

---
