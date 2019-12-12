import * as fastifyCore from 'fastify';
import * as fastifyCors from 'fastify-cors';
import * as fastifyUrlData from 'fastify-url-data';
import * as swagger from 'fastify-swagger';

import  { routes } from './routes';

interface AppOptions {
  port: number;
  listen: string;
  host: string;
  docProtocols?: string[];
}

export class App {

  protected options: AppOptions;
  public fastify: fastifyCore.FastifyInstance;

  public constructor(options: AppOptions) {
    this.options = options;
    this.fastify = fastifyCore({ logger: true });
    this.addPlugins();
    this.addRoutes();
  }

  protected addPlugins() {
    this.fastify.register(fastifyCors, {
      origin: false,
      preflight: false,
    });
    this.fastify.register(fastifyUrlData);
    this.fastify.register(swagger, {
      routePrefix: '/doc',
      exposeRoute: true,
      swagger: {
        info: {
          title: 'Transparent Partner API',
          version: '0.0.1',
        },
        host: this.options.host,
        schemes: this.options.docProtocols,
        consumes: ['application/json'],
        produces: ['application/json'],
        tags: [],
        securityDefinitions: {
          apiKey: {
            type: 'apiKey',
            name: 'apikey',
            in: 'header',
          },
        },
      },
    });
  }

  protected addRoutes() {
    this.fastify.get('/', async (_, reply) => {
      reply.type('application/json').code(200);
      return {};
    });
    this.fastify.register(routes);
  }

  public async run() {
    const address = await this.fastify.listen(this.options.port, this.options.listen);
    await this.fastify.ready();
    this.fastify.swagger();
    this.fastify.log.info(`server listening on ${address}`);
  }
}
