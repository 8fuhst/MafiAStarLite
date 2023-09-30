import { createApp } from 'vue';
import App from './App.vue';
import './index.css';

const app = createApp(App);
app.config.globalProperties.$hostname = 'http://127.0.0.1:8000/api/'
app.mount("#app");

