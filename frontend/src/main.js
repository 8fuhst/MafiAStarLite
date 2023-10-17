import { createApp } from 'vue';
import App from './App.vue';
import './index.css';

const app = createApp(App);
app.config.globalProperties.$hostname = process.env.HOSTNAME
app.mount("#app");

