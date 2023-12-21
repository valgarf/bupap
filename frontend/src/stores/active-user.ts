import { defineStore } from 'pinia';
import { provideApolloClient, useQuery } from '@vue/apollo-composable';
import { apolloClient } from 'boot/apollo';
import { gql } from '@apollo/client/core';

export enum UserState { GUEST, LOGGING_IN, LOGGED_IN };
export const useActiveUserStore = defineStore('activeUser', {
  state: () => ({
    name: null,
    fullName: null,
    state: UserState.GUEST,
    lastLoginFailed: false
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
      if (this.name == null) {
        this.lastLoginFailed = true
        this.state = UserState.GUEST;
      }
      else {
        this.state = UserState.LOGGED_IN;
      }
    },
    resultLoginHandler(result: any) {
      this.resultHander(result)
      if (this.name == null) {
        this.lastLoginFailed = true
      }
    },
    errorHandler() {
      this.state = UserState.GUEST
      this.name = null
      this.fullName = null
    },
    login(name: string, password: string) {
      if (this.state == UserState.LOGGING_IN) {
        return
      }
      this.lastLoginFailed = false
      this.state = UserState.LOGGING_IN
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
      query.onResult(this.resultLoginHandler)
      query.onError(this.errorHandler)
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
        this.state = UserState.GUEST;
      });
    }
  },
});
