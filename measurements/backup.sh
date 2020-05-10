rm -rf allbackups/influxdb
rm -rf allbackups/chronograf
mkdir -p allbackups/influxdb
mkdir -p allbackups/chronograf
sudo rm -rf influxdbbackups/*

# backup Influx DB
docker exec influxdb influxd backup -portable /backups/
sudo cp influxdbbackups/* allbackups/influxdb/

# backup Chronograf DB
sudo cp chronografdata/bolt.db allbackups/chronograf/