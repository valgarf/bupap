<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar class="q-py-md">
        <q-btn flat icon="home" aria-label="Home" to="/"/>
        <q-btn flat label="Teams" to="/teams"/>
        <q-btn flat label="Users" to="/users"/>
        <q-btn flat label="Projects" to="/projects"/>

        <q-toolbar-title>
        </q-toolbar-title>

        <q-btn flat icon="admin_panel_settings" aria-label="Admin Control" to="/admin-settings"/>
        <q-btn flat icon="settings" aria-label="Settings" to="/user-settings"/>
        <q-btn flat icon="logout" aria-label="Logout" @click="logout"/>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
function logout() {
  console.log('Implement logout');
}
</script>
