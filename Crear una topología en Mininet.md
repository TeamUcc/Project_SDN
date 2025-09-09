

# **Qué hacer después de instalar ONOS y Mininet??**

---

## **1. Confirmar que todo está funcionando correctamente**

Antes de pasar a algo más complejo, verifica que ONOS y Mininet se comunican bien.

### **a) Ejecutar ONOS**

Si no está corriendo:

```bash
docker start onos
```

Verifiquen:

```bash
docker ps
```

Debe mostrales algo asi:

```
CONTAINER ID   IMAGE              STATUS          PORTS
abcd1234efgh   onosproject/onos   Up 1 min        0.0.0.0:6653->6653/tcp, 0.0.0.0:8181->8181/tcp
```

---

### **b) Crear una topología en Mininet**

Por ejemplo, una topología tipo árbol:

```bash
sudo mn --topo tree,2 --controller=remote,ip=<IP_UBUNTU>,port=6653 --switch ovs,protocols=OpenFlow13
```

> Reemplaza `<IP_UBUNTU>` por la IP que obtuviste con:
>
> ```bash
> ip a
> ```

---

### **c) Verificar en ONOS**

1. Abre en tu navegador:

   ```
   http://<IP_UBUNTU>:8181/onos/ui
   ```
2. Usuario: `admin`
   Contraseña: `rocks`
3. Ve a la pestaña **Topology → Devices**

   * Debes ver tus switches (`s1`, `s2`, `s3`).
   * En **Hosts**, tus nodos (`h1`, `h2`, etc.).

---

### **d) Probar conectividad**

Dentro de Mininet:

```bash
pingall
```

Si todo está correcto:

```
*** Results: 0% dropped (12/12 received)
```

>  Esto confirma que **ONOS está controlando la red**.

---

## **2. Familiarizarte con la GUI de ONOS**

La GUI de ONOS es clave para monitorear tu red.

* **Topology:** visualiza switches, hosts y enlaces.
* **Devices:** información detallada de cada switch.
* **Flows:** reglas que ONOS ha instalado en los switches.
* **Intents:** abstracciones de alto nivel para definir conexiones entre hosts.

 **Objetivo:** aprender a identificar cómo ONOS maneja el flujo de tráfico en tu red.

---

## **3. Trabajar con Intents en ONOS**

Los *intents* son una forma de indicarle a ONOS qué quieres que ocurra en la red, sin preocuparte por los detalles de bajo nivel.

Ejemplo: conectar `h1` con `h4` directamente.

### **Usando la CLI de ONOS:**

Conéctate a ONOS vía SSH:

```bash
ssh -p 8101 onos@<IP_UBUNTU>
```

Contraseña: `rocks`

Comandos básicos:

```bash
apps -a             # Lista de aplicaciones disponibles
app activate org.onosproject.fwd   # Activa la aplicación de reenvío automático
```

Esto hará que ONOS instale flujos básicos automáticamente.

---

## **4. Crear topologías personalizadas**

Puedes diseñar tus propias topologías para simular redes reales.

Ejemplo:

```bash
sudo mn --custom my_topo.py --topo mynetwork --controller=remote,ip=<IP_UBUNTU>,port=6653 --switch ovs,protocols=OpenFlow13
```

Archivo `my_topo.py`:

```python
from mininet.topo import Topo

class MyNetwork(Topo):
    def build(self):
        # Hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Enlaces
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(s1, s2)
        self.addLink(h3, s2)

topos = {'mynetwork': (lambda: MyNetwork())}
```

---

## **5. Explorar los flujos instalados**

En ONOS GUI → **Flows**, revisa cómo se configuran las reglas en cada switch.

Desde la CLI de ONOS:

```bash
flows
```

Esto te permitirá entender cómo se enruta el tráfico y cómo ONOS programa los switches.

---

## **6. Desarrollar tu propia aplicación SDN en ONOS**

Si tu proyecto implica **crear una aplicación**, ONOS permite extender sus funcionalidades usando **Java + Maven**.

### **Pasos:**

1. Clona el repositorio oficial:

   ```bash
   git clone https://github.com/opennetworkinglab/onos.git
   cd onos
   ```
2. Crea un proyecto base:

   ```bash
   tools/build/onos-create-app
   ```
3. Edita tu aplicación (en Java).
4. Compílala:

   ```bash
   mvn clean install
   ```
5. Instálala en ONOS vía CLI:

   ```bash
   app install target/myapp.oar
   ```

**Objetivo:** implementar lógica personalizada, como balanceo de carga, detección de fallos o control de QoS.

---

## **7. Integrar protocolos avanzados**

Una vez domines lo básico, puedes experimentar con:

* **OpenFlow 1.3+** → ya soportado por Mininet y ONOS.
* **BGP** → simular redes más complejas.
* **P4 Runtime** → programar el plano de datos.
* **SDN + NFV** → integrar funciones de red virtualizadas.

---

## **8. Documentar resultados**

Si tu proyecto es académico, documenta:

* Topología utilizada (diagrama).
* Configuración de ONOS y Mininet.
* Resultados de las pruebas (`pingall`, reglas de flujo, capturas de pantalla).
* Conclusiones sobre el comportamiento de la red.

Herramientas recomendadas:

* **Wireshark** para analizar tráfico:

  ```bash
  sudo apt install wireshark -y
  ```
* **Draw\.io** o **Lucidchart** para diagramas.

---

## **9. Flujo final de trabajo**

1. **Iniciar ONOS:**

   ```bash
   docker start onos
   ```

2. **Verificar IP de Ubuntu:**

   ```bash
   ip a
   ```

3. **Lanzar Mininet:**

   ```bash
   sudo mn --topo tree,2 --controller=remote,ip=<IP>,port=6653 --switch ovs,protocols=OpenFlow13
   ```

4. **Verificar en ONOS GUI:**

   ```
   http://<IP>:8181/onos/ui
   ```

5. **Probar conectividad:**

   ```bash
   pingall
   ```

6. **Explorar y modificar flujos:**

   * GUI → pestaña **Flows**.
   * CLI ONOS → `flows`.

7. **Crear topologías personalizadas** y **desarrollar aplicaciones**.

---

## **10. Roadmap de aprendizaje**

| Etapa          | Actividad                                             | Objetivo                   |
| -------------- | ----------------------------------------------------- | -------------------------- |
| **Básico**     | Instalar ONOS y Mininet, usar GUI y CLI               | Entender SDN               |
| **Intermedio** | Crear topologías personalizadas, trabajar con Intents | Simular escenarios reales  |
| **Avanzado**   | Crear apps ONOS, integrar BGP, QoS, balanceo          | Desarrollar soluciones SDN |
| **Experto**    | Integrar P4 Runtime, SDN + NFV, despliegue en la nube | Redes programables reales  |

---
