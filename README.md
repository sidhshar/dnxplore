# dnxplore
Xploring Django Ninja 

# Setup docker based MySQL on Ubuntu

sudo apt update
sudo apt upgrade
sudo apt install docker.io -y

sudo systemctl start docker
sudo systemctl enable docker
docker --version
sudo docker pull mysql:latest
sudo docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=<rootpassword> -d -p 3306:3306 mysql:latest
sudo docker exec -it mysql-container mysql -u root -p

CREATE DATABASE dbspeedscan;
CREATE USER 'speedscanuser'@'%' IDENTIFIED BY '13e9f6d024Z66874';
GRANT ALL PRIVILEGES ON dbspeedscan.* TO 'speedscanuser'@'%';
FLUSH PRIVILEGES;
EXIT;

# Manage MySql container
sudo docker logs mysql-container
sudo docker start mysql-container
sudo docker stop mysql-container


# For Ubuntu

```
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install -r requirements.txt
```
