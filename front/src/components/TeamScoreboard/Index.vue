<template>
    <div v-if="error !== null">
        {{ error }}
    </div>
    <div v-else-if="team !== null" class="table">
        <div class="row">
            <div class="number">#</div>
            <div class="team">team</div>
            <div class="score">score</div>
            <div class="service-name">
                <div v-for="{ name } in tasks" :key="name" class="service-cell">
                    {{ name }}
                </div>
            </div>
        </div>
        <div>
            <div class="row" v-for="(state, index) in states" :key="index">
                <div class="number">
                    {{ state.round }}
                </div>
                <div class="team">
                    <div class="team-name">{{ team.name }}</div>
                    <div class="ip">{{ team.ip }}</div>
                </div>
                <div class="score">
                    {{ state.score.toFixed(2) }}
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
                        } in state.tasks"
                        :key="id"
                        class="service-cell"
                        :style="{
                            'font-size': `${1 - tasks.length / 20}em`,
                        }"
                        :class="`status-${status}`"
                    >
                        <button v-if="message" class="info">
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
                            {{ defense.toFixed(2) }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Team from '@/models/team';
import TeamTask from '@/models/teamTask';
import { serverUrl } from '@/config';

export default {
    props: {
        updateRound: Function,
        updateRoundStart: Function,
    },

    data: function() {
        return {
            error: null,
            team: null,
            teamId: null,
            tasks: null,
            round: 0,
            by_task: [],
        };
    },

    created: async function() {
        this.teamId = this.$route.params.id;
        try {
            const { data: scoreboard } = await this.$http.get(
                `${serverUrl}/api/scoreboard`
            );
            let { data: states } = await this.$http.get(
                `${serverUrl}/api/teams/${this.teamId}`
            );
            this.team = new Team(
                scoreboard.teams.filter(
                    ({ teamId }) => teamId == this.teamId
                )[0],
                []
            );
            this.tasks = scoreboard.services.sort(
                ({ serviceId: idA }, { serviceId: idB }) => idA - idB
            ).map(s => ({
                name: s.serviceName,
            }));

            this.round = states.reduce(
                (acc, { round }) => Math.max(acc, round),
                0
            );

            this.updateRound(this.round);

            states = states.map(s => ({
                round: s.round,
                score: s.totalPoints,
                tasks: s.serviceDetails.map(s => new TeamTask(s)).sort(
                    ({ taskId: i1 }, { taskId: i2 }) => {
                        return i1 - i2;
                    }
                ),
            }));

            this.states = states.sort(({ round: r1 }, { round: r2 }) => {
                return r2 - r1;
            });
        } catch (e) {
            this.error = "Can't connect to server";
        }
    },
};
</script>

<style lang="scss" scoped>
.table {
    display: flex;
    flex-flow: column nowrap;
    background-color: #ffffff;

    & > :first-child > :not(:last-child) {
        font-weight: bold;
        padding-top: 0.6em;
        padding-bottom: 0.6em;
        background-color: #2EC1D9;
        color: #ffffff;
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
        border-top: 1px solid #c6cad1;
        word-wrap: break-word;
        min-width: 0;
    }

    & > :first-child {
        border-left: 1px solid #c6cad1;
    }

    & > :last-child {
        border-right: 1px solid #c6cad1;
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
    flex: 3 1 10%;
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
    background-color: #2ec1d9;
    color: #ffffff;
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
</style>
