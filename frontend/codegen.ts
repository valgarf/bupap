import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  overwrite: true,
  schema: 'http://localhost:8124/graphql',
  documents: 'src/**/*.vue',
  generates: {
    'src/gql/': {
      preset: 'client',
      plugins: [],
    },
    './graphql.schema.json': {
      plugins: ['introspection'],
    },
    'src/gql/schema.graphql': {
      plugins: ['schema-ast'],
    },
  },
};

export default config;