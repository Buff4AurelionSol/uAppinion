import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router/index.js";
import { VueQueryPlugin } from "@tanstack/vue-query";
import VueApexCharts from "vue3-apexcharts";

createApp(App).use(router).use(VueQueryPlugin).use(VueApexCharts).mount("#app");
