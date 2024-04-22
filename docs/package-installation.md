# 02.0 Package Installation

### 02.1 Update and Upgrade OS Packages

`sudo apt update && sudo apt full-upgrade -y`

### 02.2 Document Device Serial Number - One Time

`cat /sys/firmware/devicetree/base/serial-number`

### 02.3 Install Mosquitto Broker and Client

`sudo apt install -y mosquitto mosquitto-clients`
`sudo systemctl enable mosquitto.service`

### 02.31 Create Mosquitto Configuration File
`sudo nano /etc/mosquitto/conf.d/standard.conf`

<new file contents>
```
listener 1883
protocol mqtt
allow_anonymous true
```

`sudo systemctl restart mosquitto.service`
