## Video de instalacion:
https://www.youtube.com/watch?v=jqdTLxu7n3c



# Environment
ubuntu 22.04

# Pre Install
- $ sudo apt install git wget vim

# Install
- Install mininet 2.3.1b4
```
 $ git clone https://github.com/mininet/mininet.git
 $ cd mininet/util
 $ git checkout 2.3.1b4
 $ ./install.sh -a
```

# Install openjdk-8-jdk
```
 $ sudo apt install openjdk-8-jdk
```
  

# Append environment variable JAVA_HOME to ~/.bashrc
PONER EL COMANDO:
```
vim ~/.bashrc
```
<img width="591" height="23" alt="image" src="https://github.com/user-attachments/assets/dbc7d82a-60a9-434f-8b1f-2a1e2420bcae" />

# NOTA: 
EN LINUX PARA PONER EL SIMBOLO "~" SE PRESIONA LA COMBINACION DE TECLAS: ALT GR + Ñ


- Ya hecho el paso anterior, poner la letra i (INSERT)

<img width="587" height="770" alt="image" src="https://github.com/user-attachments/assets/432792f0-c670-4a69-b764-d58eb66ee58c" />

Copiar y pegar:
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH
```


- Para guardar los cambios presiona la tecla (escape) 
y pone el siguiente comando:
```
:wq
```

<img width="597" height="52" alt="image" src="https://github.com/user-attachments/assets/64c4b7db-df45-473a-9e23-ac47ec40c065" />

- Despues de lo anterior ejecutar este comando:
```
$ source ~/.bashrc
```
<img width="591" height="23" alt="image" src="https://github.com/user-attachments/assets/be100429-a6d0-405b-9211-402002567292" />

- Ejecutar comandos:
```
cd ../..
```
```
ls
```
<img width="597" height="36" alt="image" src="https://github.com/user-attachments/assets/502c80f8-53e6-4576-9bfc-6e09ff41984b" />

# OJO: 
A A VECES SALE ESTE ERROR (*y si no le salio ese error, no haga caso al aviso, siga derecho*) :

<img width="601" height="152" alt="image" src="https://github.com/user-attachments/assets/2ac7b24f-c5bd-4d89-b0b3-5ad3e3376c4c" />

- En ese caso *la variable de entorno PATH se ha dañado o sobrescrito*

# Solución rápida: restaurar temporalmente el PATH

- En tu terminal, ejecuta este comando:
```
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

```
- Y listo! ya puede seguir. 

# Install onos 2.0.0
- Download onos binary file:
```
sudo wget -c https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.0.0/onos-2.0.0.tar.gz
```

```
tar zxvf onos-2.0.0.tar.gz
```
# OJO: 
A A VECES SALE ESTE ERROR (*y si no le salio ese error, no haga caso al aviso, siga derecho*) :
```
tar: onos-2.0.0: No se puede efectuar mkdir: Permiso denegado
```
# SOLUCION (Ejecutar con sudo)
```
sudo tar zxvf onos-2.0.0.tar.gz

```


# Copy files in folder to /opt/onos
```
sudo mkdir /opt/onos
```

```
sudo cp -r onos-2.0.0/* /opt/onos
```

# Run onos services 
```
cd /opt/onos/bin
```
```
sudo /opt/onos/bin/onos-service start
```

# Open another terminal
- Add configuration to ~/.ssh/config
```
mkdir ~/.ssh
```

```
touch ~/.ssh/config
```

HostKeyAlgorithms +ssh-rsa
PubkeyAcceptedKeyTypes +ssh-rsa

# Connect to onos cli and activate application
```
/opt/onos/bin/onos -l onos
password: rocks
```

```
onos@root$ app activate org.onosproject.pipelines.basic
onos@root$ app activate org.onosproject.fwd
onos@root$ app activate org.onosproject.openflow
```

# Login GUI
- Open browser and type
```
localhost:8181/onos/ui
```

```
username: onos
password: rocks
```

Run Mininet And PingAll
$ sudo mn --controller remote,ip='your-ip' --switch ovs,protocols=OpenFlow13
mininet $ pingall
