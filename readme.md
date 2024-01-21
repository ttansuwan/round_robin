# Round robin API

Implementing round robin that interact with N amount of instance

## Installation

Run poetry to set up the round robin and instances

```bash
cd round-robin
poetry init
```

## Usage
Initialize the whole entire project via docker 

Change `.env.example` to `.env` before starting docker
```bash
docker-compose up
```

To add more instances, change `NO_INSTANCES` in root `.env`

## Q&A
1. How would my round robin API handle it if one of the application APIs goes down?
* The application API will be mark as inactive and will not be return to the queue. The request will continue to be tried on other API instances in the queue. 
2. How would my round robin API handle it if one of the application APIs start to go slowly? 
* Timeout and retry mechanic are placed for each request to the API instances. This prevents:
    * Request to be hanging 
    * Even after retries, instance should no longer be in the queue
* Retries should give enough chances to the API instances but if exceed the retries (3 times), the instance should be deem as inactive and removed from the queue. 
3. How would I test this application?
* Pytest (see [Round Robin Instance](./round-robin/robin/README.md))
* Hitting endpoint directly through Postman

### What can be improved?
> This is more like an afterthought and list of things I would improve if I have more time.
1. Add a scheduler to see if the inactive instances are up and put them back into the queue (aka the list of instances where the round-robin can forward the request to)
* similar concept to liveness probe 