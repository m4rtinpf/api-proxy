curl -X POST http://localhost:9901/config_dump \
  -H 'Content-Type: application/json' \
  -d '{
        "rate_limit_service": {
          "grpc_service": {
            "envoy_grpc": {
              "cluster_name": "rate_limit_cluster"
            }
          },
          "transport_api_version": "V3"
        },
        "dynamic_route_configs": [
          {
            "route_config": {
              "name": "local_route",
              "virtual_hosts": [
                {
                  "name": "local_service",
                  "domains": [ "*" ],
                  "routes": [
                    {
                      "match": {
                        "prefix": "/"
                      },
                      "route": {
                        "cluster": "some_service"
                      },
                      "rate_limits": [
                        {
                          "actions": [
                            {
                              "request_headers": {
                                "header_name": "x-forwarded-for",
                                "descriptor_key": "remote_address"
                              }
                            }
                          ],
                          "stage": 1,
                          "rate_limit": {
                            "unit": "second",
                            "requests_per_unit": 100,
                            "descriptors": [
                              {
                                "key": "remote_address",
                                "value": "192.168.100.4"
                              }
                            ]
                          }
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          }
        ]
      }'
