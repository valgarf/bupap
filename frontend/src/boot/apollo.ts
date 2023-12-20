import { ApolloClient /*, createHttpLink */ } from '@apollo/client/core'
import { ApolloClients } from '@vue/apollo-composable'
import { boot } from 'quasar/wrappers'
import { getClientOptions } from 'src/apollo'

const options = /* await */ getClientOptions(/* {app, router ...} */)
const apolloClient = new ApolloClient(options)


export default boot(
  /* async */ ({ app }) => {
    // Default client.
    const apolloClients: Record<string, ApolloClient<unknown>> = {
      default: apolloClient,
      // clientA,
      // clientB,
    }
    app.provide(ApolloClients, apolloClients)
  }
)

export {apolloClient}
