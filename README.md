# api-proxy

This project implements an "API proxy" with the following features:

- Execute the proxy function on some specified domain (for demo purposes,
  that's [http://localhost:8000](http://localhost:8000)), that is, it acts as an intermediary for client requests,
  routing them to the required destination paths
- Allows rate limiting with different criteria:
    - Source IP address
    - Destination path
    - Combinations of both
    - Other criteria (see [here](https://github.com/envoyproxy/ratelimit))
- Stores and allows consultation of proxy usage statistics
- Handles rates in excess of 50,000 requests per second  
  _Note: There's no way to validate this locally, but the architecture should allow it (more info below)_
- Provides a REST API for statistics (see below an outline to add one for control also)

## Run

This project uses docker compose to handle local deployment.
To run:

- Edit the `./ratelimit/config.yaml` file with your IP address:

    ```yaml
        # put the source IP address here
        value: $IP_ADDRESS
    ```

- Bring all containers up:

    ```shell
    docker compose up
    ```

- Access some of the paths below

## Performance tests

There are performance tests set up using k6.
To run them simply do:

```shell
./perf_tests.sh
```

## Paths

There are several paths used for the demo:

### `products` service server

[http://localhost:3000/api/v1/products](http://localhost:3000/api/v1/products)

### `sellers` service server

[http://localhost:3001/api/v1/sellers](http://localhost:3000/api/v1/sellers)

### Client-facing `products` service

[http://localhost:8000/api/v1/products](http://localhost:8000/api/v1/products)

### Client-facing `sellers` service

[http://localhost:8000/api/v1/sellers](http://localhost:8000/api/v1/sellers)

### Proxy management UI

[http://localhost:9901](http://localhost:9901)

### Current rate limit config

[http://localhost:6070/rlconfig](http://localhost:6070/rlconfig)

### Stats UI

[http://localhost:9090/](http://localhost:9090/)

### Stats REST API

[http://localhost:9090/api/v1](http://localhost:9090/api/v1)

#### Sample endpoint

[http://localhost:9090/api/v1/query?query=envoy_cluster_upstream_rq](http://localhost:9090/api/v1/query?query=envoy_cluster_upstream_rq)