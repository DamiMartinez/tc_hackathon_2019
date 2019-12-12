import { FastifyInstance } from 'fastify';


const footprintQuerySchema = {
  type: { type: 'string', enum: ['hotel', 'restaurant'] },
  area: { type: 'number' },
  capacity: { type: 'string' },
  monthlyGasConsumption: { type: 'number' },
  monthlyElectricConsumption: { type: 'number' },
  airConditioning: { type: 'boolean'},
};

export async function routes(
  fastify: FastifyInstance,
): Promise<void> {

  fastify.get(
    '/footprint',
    {
      schema: {
        querystring: footprintQuerySchema,
      },
    },
    async (request, reply) => {
      console.log(request, reply);
      return {};
    },
  );
}
