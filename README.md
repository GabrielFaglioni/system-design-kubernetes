`C:\Windows\System32\drivers\etc`
the file hosts
```
# To allow the same kube context to work on the host and the container:
127.0.0.1 kubernetes.docker.internal
127.0.0.1 mp3converter.com
127.0.0.1 rabbitmq-manager.com
# End of section
```
Então, para apontar mp3converter.com e rabbitmq-manager.com para o localhost, é necessário rodar:
```
minikube start
```
```
minikube tunnel
```