# Round robin API

Implementing round robin that interact with N amount of instance

## Installation

Run poetry to set up the round robin and instances

```bash
cd instance-demo #or round-robin
poetry init
```

## Usage
Initialize the whole entire project via docker 

Change `.env.example` to `.env` before starting docker
```bash
docker-compose up
```

To add more instances, change `NO_INSTANCES` in root `.env`
