import { createApp } from 'vue';
import App from './App.vue';
import './index.css';

const app = createApp(App);
app.config.globalProperties.$hostname = '/api/'
app.mount("#app");

