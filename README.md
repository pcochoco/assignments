environment
Os - macOS
Shell - zsh
Terminal - macOS terminal 
Docker version - 28.5.2
Git version - 2.53.0

00 docker installation


01 creating container
use of nginx 
nginx provides the role of a web server
- listens from a specific port
- receives http requests 
- responses with resources


docker build -t my-nginx .

Docker file includes 
FROM nginx:latest 
*pulls if not exists from registry

COPY app/index.html /usr/share/nginx/html/index.html

EXPOSE 80 

container port 80 mapped with pc port 8080 
docker run -d -p 8080:80 my-nginx 

http://localhost:8080


02 bind mount
host folder connected to container internal folder

docker run -d -p 8080:80 -v ~/Desktop/web-server-example:/usr/share/nginx/html --name bind-test nginx:latest
docker exec -it bind-test ls /usr/share/nginx/html

after edit by vi index.html in terminal
enter by http://localhost:8080 to see difference


03 docker volume 
storage managed by docker 



docker volume create web-content

docker run -d -p 8080:80 -v web-content:/usr/share/nginx/html web-server-example

docker exec -it 79b2ac78dd2a bash


echo "<h1>Docker Volume Test Evidence</h1>" > /usr/share/nginx/html/index.html

docker run -d -p 8080:80 \  
  --name web-new-container \
  -v web-content:/usr/share/nginx/html \
  web-server-example

docker run -d -p 8080:80 -v web-data:/usr/share/nginx/html --name volume-test nginx:latest

docker exec -it volume-test sh -c "echo 'Volume test' > /usr/share/nginx/html/volume.txt"

*both bind mount & docker volume persist data 

04 permission 
- owner : user that created the file 
- group : collection of users
- others 

managed with binary numbers
each position with order of rwx (read, write, execute)

