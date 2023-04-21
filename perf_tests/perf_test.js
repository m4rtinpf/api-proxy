import http from 'k6/http';

const productsServer='http://localhost:3000/endpoint'
const sellersServer='http://localhost:3000/items/1'
const products='http://localhost:8000/api/v1/products'
const sellers='http://localhost:8000/api/v1/sellers/items/1'

export const options = {
  discardResponseBodies: true,
  scenarios: {
    constant_request_rate: {
      executor: 'constant-arrival-rate',
      rate: 1000,
      timeUnit: '1s', // 1000 iterations per second, i.e. 1000 RPS
      duration: '10s',
      preAllocatedVUs: 10000, // how large the initial pool of VUs would be
      maxVUs: 20000, // if the preAllocatedVUs are not enough, we can initialize more
    },
  },
};

export default function () {
  http.get(products);
}
