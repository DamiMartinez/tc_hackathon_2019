import { config } from './config';
import { App } from './main';

const appOptions = {
  port: config['port'] || 3000,
  listen: config['listen'] || '127.0.0.1',
  host: config['host'] || '127.0.0.1:3000',
  docProtocols: config['documentation-protocols'] || ['http'],
};

const app = new App(appOptions);

app.run();
