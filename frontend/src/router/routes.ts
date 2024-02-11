import { RouteRecordRaw } from 'vue-router';
import MainLayout from 'layouts/MainLayout.vue';
import TeamLayout from 'layouts/TeamLayout.vue';
import UserLayout from 'layouts/UserLayout.vue';
import ProjectLayout from 'layouts/ProjectLayout.vue';
import TaskLayout from 'layouts/TaskLayout.vue';

import TeamsPage from 'pages/TeamsPage.vue';
import UsersPage from 'pages/UsersPage.vue';
import ProjectsPage from 'pages/ProjectsPage.vue';
import LoginPage from 'pages/LoginPage.vue';
import IndexPage from 'pages/IndexPage.vue';

import TeamOverviewPage from 'pages/team/OverviewPage.vue';
import TeamMembersPage from 'pages/team/MembersPage.vue';
import TeamSchedulePage from 'pages/team/SchedulePage.vue';

import UserOverviewPage from 'pages/user/OverviewPage.vue';
import UserActivityPage from 'pages/user/ActivityPage.vue';

import ProjectOverviewPage from 'pages/project/OverviewPage.vue';
import ProjectBoardPage from 'pages/project/BoardPage.vue';

import TaskOverviewPage from 'pages/task/OverviewPage.vue';
import TaskActivityPage from 'pages/task/ActivityPage.vue';

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
        redirect: { name: 'team-index' },
        component: TeamLayout,
        children: [
          { path: 'overview', name: 'team-index', component: TeamOverviewPage },
          { path: 'members', component: TeamMembersPage },
          { path: 'schedule', component: TeamSchedulePage },
        ],
      },
      {
        path: 'user/:id',
        redirect: { name: 'user-index' },
        component: UserLayout,
        children: [
          { path: 'overview', name: 'user-index', component: UserOverviewPage },
          { path: 'activity', component: UserActivityPage },
        ],
      },
      {
        path: 'project/:id',
        redirect: { name: 'project-index' },
        component: ProjectLayout,
        children: [
          {
            path: 'overview',
            name: 'project-index',
            component: ProjectOverviewPage,
          },
          { path: 'board', component: ProjectBoardPage },
        ],
      },
      {
        path: 'task/:id',
        redirect: { name: 'task-index' },
        component: TaskLayout,
        children: [
          { path: 'overview', name: 'task-index', component: TaskOverviewPage },
          { path: 'activity', component: TaskActivityPage },
        ],
      },
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
