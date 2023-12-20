import { defineStore } from 'pinia';
import { provideApolloClient, useQuery } from '@vue/apollo-composable';
import { apolloClient } from 'boot/apollo';
import { gql } from '@apollo/client/core';

export const useActiveUserStore = defineStore('activeUser', {
  state: () => ({
    name: null,
    fullName: null,
  }),
  getters: {
    // doubleCount: (state) => state.counter * 2,
  },
  actions: {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    resultHander(result: any) {
      console.info('user result:', result)
      result = result?.data?.user
      this.name = result?.name
      this.fullName = result?.fullName
    },
    login(name: string, password: string) {
      const query = provideApolloClient(apolloClient)(() => useQuery(gql`
        mutation login($name: String! $password: String!) {
          user: login(name: $name, password: $password) {
            name
            fullName
          }
        }
      `, {
        name: name,
        password: password
      }, {
        fetchPolicy: 'no-cache',
      }))
      query.onResult(this.resultHander);
    },
    fetchUser() {
      console.info('fetch user')
      const query = provideApolloClient(apolloClient)(() => useQuery(gql`
        query activeUser {
          user: activeUser {
            name
            fullName
          }
        }
      `, null, {
        fetchPolicy: 'no-cache',
      }))
      query.onResult(this.resultHander);
    },
    logout() {
      const query = provideApolloClient(apolloClient)(() => useQuery(gql`
        mutation logout {
          user: logout {
            name
            fullName
          }
        }
      `, null, {
        fetchPolicy: 'no-cache',
      }))
      // eslint-disable-next-line @typescript-eslint/no-this-alias
      const self = this;
      query.onResult(() => {
        self.name = null
        self.fullName = null
      });
    }
  },
});
