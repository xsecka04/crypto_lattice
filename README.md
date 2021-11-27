# crypto_lattice
WIP

Real-time data visualization tool for lattice-based cryptography.

## Cretion of the docker image

```bash
git clone https://github.com/xsecka04/crypto_lattice
cd crypto_lattice
docker build -t lattice .
docker run --name=babai-server -t -i lattice
```
This will start the server. To stop the server, use CTRL+C.

## Start the server

```bash
docker start babai-server
```



