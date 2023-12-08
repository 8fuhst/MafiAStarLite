import { createApp } from 'vue';
import App from './App.vue';
import './index.css';
import { VueQueryPlugin } from "vue-query";

const app = createApp(App);
app.config.globalProperties.$hostname = import.meta.env.VITE_HOSTNAME;
app.use(VueQueryPlugin);
app.mount("#app");

