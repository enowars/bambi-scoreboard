import Vue from 'vue';
import VueRouter from 'vue-router';

import Scoreboard from '@/views/Scoreboard';
import TeamScoreboard from '@/views/TeamScoreboard';

Vue.use(VueRouter);

const routes = [
    {
        path: '/:round/',
        name: 'index',
        component: Scoreboard,
    },
    {
        path: '/teams/:id/',
        name: 'team',
        component: TeamScoreboard,
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

export default router;
