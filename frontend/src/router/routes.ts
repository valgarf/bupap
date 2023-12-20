import { RouteRecordRaw } from 'vue-router';
import { default as TeamsPage } from 'pages/TeamsPage.vue';
import { default as UsersPage } from 'pages/UsersPage.vue';
import { default as ProjectsPage } from 'pages/ProjectsPage.vue';
import { default as LoginPage } from 'pages/LoginPage.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'login', component: LoginPage }, //() => import('pages/TeamsPage.vue') },
      { path: 'teams', component: TeamsPage }, //() => import('pages/TeamsPage.vue') },
      { path: 'users', component: UsersPage }, //() => import('pages/TeamsPage.vue') },
      { path: 'projects', component: ProjectsPage }, //() => import('pages/TeamsPage.vue') },
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
