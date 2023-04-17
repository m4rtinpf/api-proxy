import http from 'k6/http';

const echoServer='http://localhost:8080/'
const proxy='http://localhost:8000/api/v1/proxy/endpoint'

export const options = {
  discardResponseBodies: true,
  scenarios: {
    constant_request_rate: {
      executor: 'constant-arrival-rate',
      rate: 500,
      timeUnit: '1s', // 1000 iterations per second, i.e. 1000 RPS
      duration: '30s',
      preAllocatedVUs: 10000, // how large the initial pool of VUs would be
      maxVUs: 20000, // if the preAllocatedVUs are not enough, we can initialize more
    },
  },
};

export default function () {
  http.get(proxy);
}
