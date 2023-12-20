import { RouteRecordRaw } from 'vue-router';
import { default as TeamsPage } from 'pages/TeamsPage.vue';
import { default as UsersPage } from 'pages/UsersPage.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'teams', component: TeamsPage }, //() => import('pages/TeamsPage.vue') },
      { path: 'users', component: UsersPage }, //() => import('pages/TeamsPage.vue') },
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
