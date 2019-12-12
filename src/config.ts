import { env, ArgumentTypes } from '@trans/config';

interface Config {
  port: number;
  listen: string;
  host: string;
  'documentation-protocols': string[];
}

const paramsDefinition = [
  { name: 'port', type: Number, description: 'API listening port' },
  { name: 'listen', type: String, description: 'API address to bind' },
  { name: 'host', type: String, description: 'API host address' },
  { name: 'prefix', type: String, description: 'API prefix for routes' },
  { name: 'documentation-protocols', type: ArgumentTypes.arrayOf(String),
    description: 'Protocols in the selector in swagger', defaultValue: ['https'] },
];

env.load();

export const config: Config = env.getArguments(
  paramsDefinition,
  process.argv,
  { handleHelp: true },
) as Config;
