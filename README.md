# Net Calc

An IPv4/IPv6 calculator built with Python/Flask.

## Build Docker Image Locally

```bash
docker build -t netcalc:latest .
```

If using Mac OS with M1 ARM cpu, build using

```bash
docker build --no-cache --platform linux/amd64 -t netcalc:latest .
```

Run the image locally

```bash
docker run -d -p 8080:8080 netcalc:latest
```

push image to Azure Container registry

```bash
az login
az acr login --name tpulliam
docker tag subnet_calc:latest tpulliam.azurecr.io/subnet_calc:latest
docker push tpulliam.azurecr.io/subnet_calc:latest
```

Naviagate to `http://localhost:8080`

## Configure a GitHub Action to create a container instance

https://learn.microsoft.com/en-us/azure/container-instances/container-instances-github-action?tabs=userlevel
