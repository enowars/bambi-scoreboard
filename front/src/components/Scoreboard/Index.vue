<template>
    <div v-if="error !== null">{{ error }}</div>
    <div v-else-if="teams !== null" class="table">
        <div class="row">
            <div class="number">#</div>
            <div class="team">team</div>
            <div class="score">score</div>
            <div class="service-name">
                <div :key="name" class="service-cell" v-for="{ name } in tasks">
                    {{ name }}
                </div>
            </div>
        </div>
        <transition-group name="teams-list">
            <div
                class="row"
                v-for="({ name, score, tasks, ip, id, highlighted },
                index) in teams"
                :key="name"
                :class="[`top-${index + 1}`, highlighted ? 'highlighted' : '']"
            >
                <div
                    class="number"
                    :class="[
                        `top-${index + 1}`,
                        index > 2 ? 'default-team' : '',
                        highlighted ? 'pd-3-left' : '',
                        highlighted ? 'pd-3-topbottom' : '',
                    ]"
                >
                    {{ index + 1 }}
                </div>
                <div
                    class="team team-row"
                    @click="openTeam(id)"
                    :class="[
                        `top-${index + 1}`,
                        index > 2 ? 'default-team' : '',
                        highlighted ? 'pd-3-topbottom' : '',
                    ]"
                >
                    <div class="team-name">{{ name }}</div>
                    <div class="ip">{{ ip }}</div>
                </div>
                <div
                    class="score"
                    :class="[
                        `top-${index + 1}`,
                        index > 2 ? 'default-team' : '',
                        highlighted ? 'pd-3-topbottom' : '',
                    ]"
                >
                    {{ score.toFixed(2) }}
                </div>
                <div class="service">
                    <div
                        v-for="{
                            id,
                            sla,
                            attack,
                            defense,
                            message,
                            status,
                        } in tasks"
                        :key="id"
                        class="service-cell"
                        :style="{
                            'font-size': `${1 - tasks.length / 20}em`,
                        }"
                        :class="`status-${status}`"
                    >
                        <button class="info">
                            <i class="fas fa-info-circle" />
                            <span class="tooltip">{{
                                message === '' ? 'OK' : message
                            }}</span>
                        </button>
                        <div class="sla">
                            <i class="fas fa-tachometer-alt" />
                            {{ sla.toFixed(2) }}
                        </div>
                        <div class="attack">
                            <i class="fas fa-flag" />
                            {{ attack.toFixed(2) }}
                        </div>
                        <div class="defense">
                            <i class="fas fa-shield-alt" />
                            -{{ defense.toFixed(2) }}
                        </div>
                    </div>
                </div>
            </div>
        </transition-group>
    </div>
</template>

<script>
import { serverUrl } from '@/config';
import Task from '@/models/task';
import Team from '@/models/team';
import axios from 'axios';

export default {
    props: {
        updateRound: Function,
        updateRoundTime: Function,
        updateRoundStart: Function,
        timer: Number,
    },

    data: function() {
        return {
            error: null,
            server: null,
            tasks: null,
            teams: null,
            round_start: 0,
        };
    },

    methods: {
        openTeam: function(id) {
            clearInterval(this.timer);
            this.$router.push({ name: 'team', params: { id } }).catch(() => {});
        },
    },

    created: async function() {
        let r;
        while (!r) {
            try {
                r = await axios.get(`${serverUrl}/api/scoreboard`);
                break;
            } catch (err) {
                console.log('Failed to fetch scoreboard: ' + err);
                await new Promise(r => setTimeout(r, 2000));
            }
        }

        const {
            CurrentRound: round,
            StartTimeEpoch: round_start,
            EndTimeEpoch: round_end,
            Services: tasks,
            Teams: teams,
        } = r.data;

        this.updateRoundStart(round_end);
        this.updateRoundTime(round_end - round_start);
        console.log(this.roundTime);
        console.log(round_end);
        console.log(new Date().getTime() / 1000);
        this.updateRound(round);
        this.tasks = tasks.map(task => new Task(task)).sort(Task.comp);
        this.teams = teams
            .map(
                team =>
                    new Team(team, this.tasks)
            )
            .sort(Team.comp);

        while (this.teams) {
            try {
                r = await axios.get(`${serverUrl}/api/scoreboard/live`);
                const {
                    CurrentRound: round,
                    StartTimeEpoch: round_start,
                    EndTimeEpoch: round_end,
                    Services: tasks,
                    Teams: teams,
                } = r.data;
                this.updateRoundStart(round_end);
                this.updateRoundTime(round_end - round_start);
                this.updateRound(round);
                teams.forEach(incoming_team => {
                    this.teams.forEach(team => {
                        team.update(incoming_team);
                    });
                });
                this.teams = this.teams.sort(Team.comp);
            } catch (err) {
                console.log('Failed to fetch scoreboard: ' + err);
                await new Promise(r => setTimeout(r, 2000));
            }
        }
    },
};
</script>

<style lang="scss" scoped>
.pd-3-left {
    margin-left: 2px;
}
.pd-3-topbottom {
    margin-top: 2px;
    margin-bottom: 2px;
}

.default-team {
    background-color: white;
}

.team-row {
    cursor: pointer;
}

.teams-list-move {
    transition: transform 1s;
}

.table {
    display: flex;
    flex-flow: column nowrap;

    & > :first-child > :not(:last-child) {
        font-weight: bold;
        padding-top: 0.6em;
        padding-bottom: 0.6em;
    }

    & > :not(:first-child) > * {
        height: 6em;
    }

    & > :last-child > :last-child > * {
        border-bottom: 1px solid #c6cad1;
    }
}

.row {
    display: flex;
    flex-flow: row nowrap;
    text-align: center;

    & > * {
        word-wrap: break-word;
        min-width: 0;
    }

    border-top: 1px solid #c6cad1;
    border-left: 1px solid #c6cad1;
    border-right: 1px solid #c6cad1;

    &.highlighted > * {
        padding-top: 3px;
        padding-bottom: 3px;
    }

    &.highlighted > :first-child {
        padding-left: 3px;
    }

    &.highlighted > :last-child {
        padding-right: 3px;
    }
}

.team-name {
    font-weight: bold;
}

.number {
    flex: 1 1 0;
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
}

.team {
    flex: 3 1 15%;
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
}

.score {
    flex: 2 1 5%;
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
}

.service {
    flex: 20 2 0;
    display: flex;
    flex-flow: row nowrap;

    border-left: 1px solid #c6cad1;

    & > :not(:last-child) {
        border-right: 1px solid #c6cad1;
    }
}

.service-name {
    flex: 20 2 0;
    display: flex;
    flex-flow: row nowrap;
    text-align: center;
}

.service-cell {
    flex: 1 1 0;

    position: relative;

    display: flex;
    flex-flow: column nowrap;
    justify-content: space-around;
}

.sla {
    text-align: left;
    margin-left: 0.5em;
}

.attack {
    text-align: left;
    margin-left: 0.5em;
}

.defense {
    text-align: left;
    margin-left: 0.5em;
}

.info {
    padding: 0;
    position: absolute;
    top: 0.5em;
    left: calc(100% - 2.5em - 0.5em);
    width: 2.5em;
    height: 2.5em;

    border-radius: 0.3em;
    font-size: 0.7em;
    border: 1px solid #c6cad1;

    &:focus {
        outline: 0;
        border: 1px solid #c6cad1;
    }
}

.tooltip {
    font-size: 0.7rem;
    left: 0;
    top: 0;
    transform: translateX(calc(-100%)) translateY(calc(-100% - 0.25em));
    position: absolute;
    width: 20em;
    text-align: center;
    display: block;
    background-color: black;
    color: white;
    border-radius: 0.5em;
    padding: 1em;
    opacity: 0;
    z-index: -1;
}

.info:hover .tooltip {
    opacity: 1;
    z-index: 1;
}

.highlighted {
    transform: translateZ(0);
    animation: rotate 5s infinite linear;
    background: rgb(48, 255, 144); /* Old browsers */
    background: linear-gradient(
        to right,
        rgba(48, 255, 144, 1) 0%,
        rgba(237, 45, 237, 1) 25%,
        rgba(201, 152, 38, 1) 50%,
        rgba(48, 255, 230, 1) 75%,
        rgba(48, 255, 144, 1) 100%
    );
}

@keyframes rotate {
    from {
        background-position: -3000px;
    }
    to {
        background-position: 0px;
    }
}
</style>
