
#### 1. **Intento inicial de ejecutar el contenedor**

El primer intento de lanzar el contenedor fue con el siguiente comando:

```bash
docker run -d --name onos -p 8181:8181 -p 8101:8101 -p 6653:6653 onosproject/onos
```

Este comando intenta lo siguiente:

* **`docker run -d`**: Ejecuta el contenedor en modo desacoplado (en segundo plano).
* **`--name onos`**: Asigna el nombre `onos` al contenedor.
* **`-p 8181:8181 -p 8101:8101 -p 6653:6653`**: Mapea los puertos del contenedor a puertos en el host local. Esto permite acceder a los servicios en esos puertos.

#### 2. **Problema: El contenedor ya existía**

Después de intentar ejecutar el contenedor, se encontró el siguiente error:

```
docker: Error response from daemon: Conflict. The container name "/onos" is already in use by container "73604f74bb5721b2dcf97dc5c59ec9e5ceea46967b13d58ced49d590a69a86ed". You have to remove (or rename) that container to be able to reuse that name.
```

Esto sucedió porque ya había un contenedor llamado `onos` previamente creado que no estaba corriendo en ese momento.

#### 3. **Verificación del estado de los contenedores**

Para comprobar qué contenedores están en ejecución y sus estados, ejecutamos el comando:

```bash
docker ps -a
```

Esto mostró que había un contenedor llamado `onos` que estaba detenido y que estaba causando el conflicto. El contenedor tenía el siguiente estado:

```
CONTAINER ID   IMAGE              COMMAND                  CREATED        STATUS                      PORTS                                                                                                                                                 NAMES
73604f74bb57   onosproject/onos   "./bin/onos-service …"   45 hours ago   Exited (255) 23 hours ago   0.0.0.0:6653->6653/tcp, :::6653->6653/tcp, 0.0.0.0:8101->8101/tcp, :::8101->8101/tcp, 6640/tcp, 9876/tcp, 0.0.0.0:8181->8181/tcp, :::8181->8181/tcp   onos
```

El contenedor `onos` estaba detenido con un código de salida `255`, lo que indica que algo pudo haber fallado en su inicio.

#### 4. **Eliminación del contenedor antiguo**

Decidimos eliminar el contenedor detenido para liberar el nombre `onos` y evitar conflictos. Para ello, usamos el siguiente comando:

```bash
docker rm onos
```

Este comando eliminó el contenedor llamado `onos`.

#### 5. **Reiniciar el contenedor `onos`**

Una vez que eliminamos el contenedor antiguo, ejecutamos nuevamente el comando para crear y ejecutar un nuevo contenedor:

```bash
docker run -d --name onos -p 8181:8181 -p 8101:8101 -p 6653:6653 onosproject/onos
```

Al ejecutar este comando, Docker creó y puso en marcha un nuevo contenedor con la imagen `onosproject/onos`.

#### 6. **Verificación del contenedor en ejecución**

Para asegurarnos de que el contenedor estaba corriendo, ejecutamos el siguiente comando:

```bash
docker ps
```

Esto nos mostró el siguiente estado:

```
CONTAINER ID   IMAGE              COMMAND                  CREATED              STATUS              PORTS                                                                                                                                                 NAMES
dccc341a5536   onosproject/onos   "./bin/onos-service …"   About a minute ago   Up About a minute   0.0.0.0:6653->6653/tcp, :::6653->6653/tcp, 0.0.0.0:8101->8101/tcp, :::8101->8101/tcp, 6640/tcp, 9876/tcp, 0.0.0.0:8181->8181/tcp, :::8181->8181/tcp   onos
```

Esto indica que el contenedor está en ejecución, y los puertos han sido mapeados correctamente.

#### 7. **Intento de eliminar un contenedor en ejecución**

Intentamos eliminar el contenedor mientras estaba corriendo, pero Docker no lo permitió porque el contenedor está activo. Para eliminar un contenedor en ejecución, primero debes detenerlo con:

```bash
docker stop onos
```

Y luego puedes eliminarlo:

```bash
docker rm onos
```

O, si necesitas forzar la eliminación sin detener el contenedor, puedes usar:

```bash
docker rm -f onos
```

#### 8. **Verificación final**

Finalmente, con `docker ps` confirmamos que el contenedor estaba en ejecución, y todo estaba listo para ser usado.

---

### Resumen

* **El contenedor `onos` fue lanzado correctamente** y está funcionando en el puerto 8181, 8101 y 6653.
* **El contenedor anterior** fue eliminado para resolver el conflicto de nombre.
* **Docker está corriendo** el contenedor y está mapeando los puertos correctamente para que puedas acceder a los servicios.

---


---

¿Te gustaría realizar alguna prueba o necesitas ayuda adicional con alguna parte del proceso?
