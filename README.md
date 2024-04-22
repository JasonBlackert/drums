# Drums

## Dog Run Monitoring System

### Step 1.0 Build
`docker run -u 1000 --rm -itv $PWD:/workspace $(docker build -f drums-mqtt/Dockerfile -q .) `

### Step 2.0 Copy to Device
`scp drums-mqtt_0.1.0-1_all.deb target@target-ip:`

### Step 2.1 Install on Target Device
`sudo dpkg -i drums-mqtt_0.1.0-1_all.deb`

If install doesn't succeed - fix broken
`sudo apt --fix-broken install`