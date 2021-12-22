# crypto_lattice
WIP

Real-time data visualization tool for lattice-based cryptography.

## Cretion of the docker image

```bash
git clone https://github.com/xsecka04/crypto_lattice
cd crypto_lattice
docker build -t babai .
docker run -d -p 50000:50000 -p 50007:50007 --name=babai-server -t -i babai
```
This will start the server. To stop the server, use 

```bash
docker stop babai-server
```

## Start the server

```bash
docker start babai-server
```



