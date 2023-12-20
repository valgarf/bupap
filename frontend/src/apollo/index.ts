import type { ApolloClientOptions } from '@apollo/client/core'
import { createHttpLink, InMemoryCache, ApolloLink } from '@apollo/client/core'
import type { BootFileParams } from '@quasar/app-vite'
import { onError } from '@apollo/client/link/error';
import { Notify } from 'quasar'

export /* async */ function getClientOptions(
  // eslint-disable-next-line @typescript-eslint/no-unused-vars, @typescript-eslint/no-explicit-any
  /* {app, router, ...} */ options?: Partial<BootFileParams<any>>
) {

  // See https://nerdydiary.medium.com/setting-a-custom-timeout-with-apollo-client-in-your-next-react-native-project-704dcc3c17fc
  // for explanation of the timeout and erro handling logic.
  function fetchWithTimeout(uri: string, options = {}, time: number): Promise<Response> {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        reject(new Error('Request timed out.'));
      }, time);
      fetch(uri, options).then(
        response => {
          clearTimeout(timer);
          resolve(response);
        },
        err => {
          clearTimeout(timer);
          reject(err);
        }
      );
    });
  }

  
  const httpLink = createHttpLink({
    uri:
      process.env.GRAPHQL_URI ||
      // Change to your graphql endpoint.
      '/graphql',
    fetch: (uri: string, options: any) => {
      const timeoutFromHeader = options?.headers?.['x-timeout'];
      const timeout = timeoutFromHeader || Number(process.env.DEFAULT_TIMEOUT) || 5000;
      return fetchWithTimeout(uri, options, timeout);
    }
  })


  const errorLink = onError(({ graphQLErrors, networkError }) => {
    let errMsg: string|null = null;
    if (networkError) {
      errMsg = `Network Error: ${networkError.message}`
    }
    if (graphQLErrors) {
      const gqlErr = graphQLErrors.map((error) => error.message || JSON.stringify(error));
      errMsg = `GraphQL Error: ${gqlErr}`
    }
    if (errMsg != null) {
      console.error(errMsg);
      Notify.create(
        {
          message: 'GraphQL query failed',
          color: 'negative',
          caption: errMsg,
          actions: [
            { icon: 'close', round: true, color: 'white', handler: () => { /* ... */ } }
          ]
        });
    }    
  });

  return <ApolloClientOptions<unknown>>Object.assign(
    // General options.
    <ApolloClientOptions<unknown>>{
      link: ApolloLink.from([errorLink, httpLink]),

      cache: new InMemoryCache(),
    },

    // Specific Quasar mode options.
    process.env.MODE === 'spa'
      ? {
          //
        }
      : {},
    process.env.MODE === 'ssr'
      ? {
          //
        }
      : {},
    process.env.MODE === 'pwa'
      ? {
          //
        }
      : {},
    process.env.MODE === 'bex'
      ? {
          //
        }
      : {},
    process.env.MODE === 'cordova'
      ? {
          //
        }
      : {},
    process.env.MODE === 'capacitor'
      ? {
          //
        }
      : {},
    process.env.MODE === 'electron'
      ? {
          //
        }
      : {},

    // dev/prod options.
    process.env.DEV
      ? {
          //
        }
      : {},
    process.env.PROD
      ? {
          //
        }
      : {},

    // For ssr mode, when on server.
    process.env.MODE === 'ssr' && process.env.SERVER
      ? {
          ssrMode: true,
        }
      : {},
    // For ssr mode, when on client.
    process.env.MODE === 'ssr' && process.env.CLIENT
      ? {
          ssrForceFetchDelay: 100,
        }
      : {}
  )
}
