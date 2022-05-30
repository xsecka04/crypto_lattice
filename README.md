# crypto_lattice
WIP

Real-time data visualization tool for lattice-based cryptography.

## Cretion of the docker image

```bash
git clone https://github.com/xsecka04/crypto_lattice
cd crypto_lattice
docker build -t lattice .
docker run -d -p 50000:50000 -p 50007:50007 --name=lattice-server -t -i lattice
```
This will start the server. To stop the server, use 

```bash
docker stop lattice-server
```

## Start the server

```bash
docker start lattice-server
```



