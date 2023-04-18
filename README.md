# api-proxy

## Echo server

https://github.com/ErikWegner/rsecho

```shell
docker run -p 3000:3000 erikwegner/rsecho
```

## Envoy

```shell
docker rm /envoy && docker build -t envoy:v1 . && docker run -d --network=host --name envoy envoy:v1

```

## FastAPI

Max 2k RPS

## License

This project is licensed under the terms of the MIT license.
