<template>
  <div class="flex flex-col min-h-screen min-v-screen">
    <SiteContent/>
    <DefaultFooter/>
  </div>
</template>

<script>
import DefaultNavbar from "./components/DefaultNavbar.vue";
import SiteContent from "./components/SiteContent.vue";
import DefaultFooter from "./components/Footer.vue";

export default {
  name: 'App',
  components: {
    DefaultFooter,
    SiteContent,
    DefaultNavbar,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
