import { RouteRecordRaw } from 'vue-router';
import { default as MainLayout } from 'layouts/MainLayout.vue';
import { default as TeamLayout } from 'layouts/TeamLayout.vue';
import { default as UserLayout } from 'layouts/UserLayout.vue';

import { default as TeamsPage } from 'pages/TeamsPage.vue';
import { default as UsersPage } from 'pages/UsersPage.vue';
import { default as ProjectsPage } from 'pages/ProjectsPage.vue';
import { default as LoginPage } from 'pages/LoginPage.vue';
import { default as IndexPage } from 'pages/IndexPage.vue';

import { default as TeamOverviewPage } from 'pages/team/OverviewPage.vue';
import { default as TeamMembersPage } from 'pages/team/MembersPage.vue';
import { default as TeamSchedulePage } from 'pages/team/SchedulePage.vue';

import { default as UserOverviewPage } from 'pages/user/OverviewPage.vue';
import { default as UserActivityPage } from 'pages/user/ActivityPage.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: MainLayout, //() => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: IndexPage }, //() => import('pages/IndexPage.vue') },
      { path: 'login', component: LoginPage }, 
      { path: 'teams', component: TeamsPage }, 
      { path: 'users', component: UsersPage }, 
      { path: 'projects', component: ProjectsPage }, 
      {
        path: 'team/:id',
        redirect: {name:'team-index'},
        component: TeamLayout,
        children: [
          { path: 'overview', name: 'team-index', component: TeamOverviewPage},
          { path: 'members', component: TeamMembersPage}, 
          { path: 'schedule', component: TeamSchedulePage}, 
        ]
      },
      {
        path: 'user/:id',
        redirect: {name:'user-index'},
        component: UserLayout,
        children: [
          { path: 'overview', name: 'user-index', component: UserOverviewPage}, 
          { path: 'activity', component: UserActivityPage}, 
        ]
      },
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
