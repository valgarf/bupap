<template>
  <q-layout view="hHh lpR fFf">
    <q-header>
      <q-toolbar class="q-py-md">
        <q-btn flat icon="home" aria-label="Home" to="/" />
        <q-btn flat label="Teams" to="/teams" />
        <q-btn flat label="Users" to="/users" />
        <q-btn flat label="Projects" to="/projects" />

        <q-toolbar-title> </q-toolbar-title>

        <q-btn
          flat
          v-if="user.name != null"
          icon="admin_panel_settings"
          aria-label="Admin Control"
          to="/admin-settings"
        />
        <q-btn
          flat
          v-if="user.name != null"
          icon="settings"
          aria-label="Settings"
          to="/user-settings"
        />
        <q-btn
          flat
          v-if="user.name != null"
          icon="logout"
          aria-label="Logout"
          @click="logout"
        />
        <q-btn
          flat
          v-if="user.name == null"
          icon="login"
          aria-label="Login"
          to="/login"
        />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { useActiveUserStore } from 'src/stores/active-user';
import { useRouter } from 'vue-router';
const router = useRouter();
function logout() {
  user.logout();
  router.push('/');
}
const user = useActiveUserStore();
user.fetchUser();
</script>
