Instructions for Raspberry Pi Zero W

# Initial setup

```
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
mkdir -p ~/.local/bin
```

# Install Docker

```
curl -fsSL https://get.docker.com -o get-docker.sh
chmod +x  get-docker.sh
sudo ./get-docker.sh
sudo usermod -aG docker pi
```

Logout, then log back in.  

Test using an ARM32 v6 Alpine image

```
docker run -it --rm arm32v6/alpine:latest /bin/sh

/ # cat /etc/os-release
```

## Install docker compose

```
pip3 install docker-compose
docker-compose --version
```


# Get InfluxDB and Chronograf


A docker-compose.yml exists for InfluxDB and Chronograf with ARM32V6 images. 

Run it

```
    cd measurements
    docker-compose up -d
```    

Wait up to 5 minutes for Influx and Chronograf to come up! 

Backup db:

    docker exec -it influxdb influxd backup -portable /backups/

Restore db:

    docker exec -it influxdb influxd restore -portable /backups/
 
 Then browse to http://raspberrypi/ for the Chronograf interface


# Set up dependencies

Some missing dependencies first. 

```
# Enviro lib
cd enviroplus
sudo ./install.sh
cd ..

# Influx lib
pip3 install influxdb
```



# Run the main sensors script

Via crontab: 

```
@reboot sleep 60 && cd /home/pi/enviro-influx-chronograf/measurements && python3 everything.py &
```

Manually:


```
cd measurements
python3 everything.py
```


# Run the pihole stats collection script

Via crontab:

```
30 * * * * cd /home/pi/enviro-influx-chronograf/measurements && python3 piholestats.py > piholestats.log 2>&1
```

Manually:

```
cd measurements
python3 piholestats.py
```

# Run the backup scripts

Via crontab:

```
00 * * * * cd /home/pi/enviro-influx-chronograf/measurements && bash backup.sh > backup.log 2>&1
```

Manually:

```
cd measurements
./backup.sh
```

