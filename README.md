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

There are performance tests set up using [k6](https://k6.io/).
To run them simply do:

```shell
./perf_tests.sh
```

## Paths

There are several paths used for the demo:

### `products` service server

[http://localhost:3000](http://localhost:3000)

### `sellers` service server

[http://localhost:3001](http://localhost:3001)

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

## Architecture

This demo uses several containers, defined on `docker-compose.yaml`.

### `proxy`

This is the main component of the project.
It's an [Envoy](https://www.envoyproxy.io/) proxy, designed for high-performance and cloud native applications.

It's configured with the `envoy.yaml` file.
This proxy listens for requests on [http://localhost:8000/](http://localhost:8000/).
If the request is directed at the `products` service (`/api/v1/products`), it forwards the request to it (`products`
container).
It works in a similar way for the `sellers` service.

This service is not providing rate limiting by itself; instead it defers to the `ratelimit` service.

It exposes a management UI and REST API on [http://localhost:9901](http://localhost:9901).
All the configuration done through `envoy.yaml` can also be done through the REST API.

It also has a gRPC server, which is used to communicate with the `ratelimit` service.

### `products` and `sellers`

These are the services where the requests from the client get routed to.
They are echo servers (they respond to any request made to them with the request info).

### `redis`

This is a [Redis](https://redis.io/) cache used by the `ratelimit` service to keep the rate limiting data.

### `ratelimit`

An [Envoy ratelimit](https://github.com/envoyproxy/ratelimit) instance that receives gRPC requests from `proxy`, checks
its configured rules, and responds if the request should be allowed through or not.

Is configured through the `ratelimit/config.yaml` file:

```yaml
---
domain: rl
descriptors:
  - key: products
    rate_limit:
      unit: second
      requests_per_unit: 200

  - key: remote_address
    # put the source IP address here
    value: $IP_ADDRESS
    rate_limit:
      unit: second
      requests_per_unit: 1000
```

This configuration (combined with the `proxy` configuration on `envoy.yaml`) sets a rate limit of:

- 200 RPS for the [http://localhost:8000/api/v1/products](http://localhost:8000/api/v1/products) destination path
- 1000 RPS for the `$IP_ADDRESS` source address

The current rule config can be accessed in [http://localhost:6070/rlconfig](http://localhost:6070/rlconfig).

The rules can't be configured through a REST API.
The preferred way to add it would be to summit a PR on the ratelimit repo (it's an open source project).
Alternatively, a shared volume could be added so that:

- A REST API allows editing a rules file (`ratelimit/config.yaml`)
- The `ratelimit` container watches for changes on this file (set the `RUNTIME_WATCH_ROOT` flag to `true`)

### `stats`

To provide usage statistics, a [Prometheus](https://prometheus.io/) service is used.

This server periodically queries the `/stats/prometheus` endpoint exposed by `proxy` to get the necessary data and
stores it in a [time series database](https://en.wikipedia.org/wiki/Time_series_database).

It provides a UI ([http://localhost:9090/](http://localhost:9090/)) and a REST
API ([http://localhost:9090/api/v1](http://localhost:9090/api/v1)).
The REST API is fairly complex; and example endpoint
is [http://localhost:9090/api/v1/query?query=envoy_cluster_upstream_rq](http://localhost:9090/api/v1/query?query=envoy_cluster_upstream_rq),
which returns the _current_ values for the `envoy_cluster_upstream_rq` metric (API
docs [here](https://prometheus.io/docs/prometheus/latest/querying/api/)).
