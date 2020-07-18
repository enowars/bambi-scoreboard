<template>
    <div class="changeRound">
        <a :href="+round - 1">Previous Round</a>
        <a :href="+round + 1">Next round</a>
    </div>
</template>

<script>
export default {
    props: {
        round: Number,
    },
    methods: {
        openRound: function(round) {
            this.$router
                .push({ name: 'index', params: { round } })
                .catch(() => {});
        },
    },
};
</script>

<style lang="scss" scoped>
.changeRound {
    position: relative;
    background: lightblue;
    padding: 1em;

    display: flex;
    flex-flow: row nowrap;

    justify-content: space-between;
    align-items: center;
}
</style>
