# subnet_calculator

## Build Docker Image Locally

```bash
docker build -t subnet_calc:latest .
```

If using Mac OS with M1 ARM cpu, build using

```bash
docker build --no-cache --platform linux/amd64 -t subnet_calc:latest .
```

Run the image locally

```bash
docker run -d -p 8080:80 subnet_calc:latest
```

push image to Azure Container registry

```bash
az login
az acr login --name subnetcalc
docker tag subnet_calc:latest subnetcalc.azurecr.io/subnet_calc:latest
docker push subnetcalc.azurecr.io/subnet_calc:latest
```

Naviagate to `http://localhost:8080`

## Configure a GitHub Action to create a container instance

https://learn.microsoft.com/en-us/azure/container-instances/container-instances-github-action?tabs=userlevel
