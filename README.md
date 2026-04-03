### environment
- Os - macOS
- Shell - zsh
- Terminal - macOS terminal 
- Docker version - 28.5.2
- Git version - 2.53.0

## 00 docker installation
- docker version
- github version 
<img width="607" height="387" alt="Screenshot 2026-04-01 at 2 05 35 PM" src="https://github.com/user-attachments/assets/cd28d408-f2a8-4978-b653-e6e9d2c50c8e" />


## 01 creating container
use of nginx 
nginx provides the role of a web server
- listens from a specific port
- receives http requests 
- responses with resources

making image 
```
docker build -t my-nginx .
```

Docker file includes 
```
FROM nginx:latest 
```
*pulls if not exists from registry

```
COPY index.html /usr/share/nginx/html/index.html
```
index.html into nginx container


```
EXPOSE 80 
```

container port 80 mapped with pc port 8080 
```docker run -d -p 8080:80 my-nginx ```

http://localhost:8080
<img width="615" height="254" alt="Screenshot 2026-04-01 at 2 42 40 PM" src="https://github.com/user-attachments/assets/72e7f81d-d504-4db1-8fa2-2367cda25552" />


## 02 bind mount
host folder connected to container internal folder

``` docker run -d -p 8080:80 -v ~/Desktop/web-server-example:/usr/share/nginx/html --name bind-test nginx:latest ```

after edit by vi index.html in terminal
enter by http://localhost:8080 to see difference

<img width="1177" height="272" alt="Screenshot 2026-04-01 at 2 25 28 PM" src="https://github.com/user-attachments/assets/ca18f3c5-2415-4f27-a470-f2093c4ce8cc" />


## 03 docker volume 
storage managed by docker 

creating volume 
```
docker volume create web-content
```

create container with volume 
```
docker run -d -p 8080:80 -v web-content:/usr/share/nginx/html web-server-example
```

use bash in container 
```
docker exec -it 79b2ac78dd2a bash
```

change index.html content 
```
echo "<h1>Docker Volume Test Evidence</h1>" > /usr/share/nginx/html/index.html
```

- delete first container 
- create a new container 
```
docker run -d -p 8080:80 \  
  --name web-new-container \
  -v web-content:/usr/share/nginx/html \
  web-server-example
```

difference added to index.html that was made on the first container 

<img width="312" height="209" alt="Screenshot 2026-04-01 at 3 28 16 PM" src="https://github.com/user-attachments/assets/5d2666c8-5c48-4864-9bf5-4374f68e099f" />

*both bind mount & docker volume persist data 

## 04 permission 
- owner : user that created the file 
- group : collection of users
- others 

managed with binary numbers
each position with order of rwx (read, write, execute)

ex) chmod u+r Dockerfile : owner reading permission granted
<br>
[example for file]
<img width="992" height="287" alt="Screenshot 2026-04-01 at 3 35 40 PM" src="https://github.com/user-attachments/assets/5472dcbd-f766-48ee-9049-bd20d6a88614" />

<br>
[example for dir]
<img width="587" height="124" alt="Screenshot 2026-04-01 at 3 33 37 PM" src="https://github.com/user-attachments/assets/60f7e5c6-7f6b-4bf2-b567-2569c986da7e" />

