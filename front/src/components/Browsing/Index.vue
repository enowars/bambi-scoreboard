<template>
    <div class="changeRound">
      <button @click="openRound(round-1)">Previous Round</button>
      <button @click="openRound(round+1)">Next round</button>
    </div>
</template>

<script>
export default {
    methods: {
        openRound: function(round) {
            this.$router.push({ name: 'scoreboard', params: { round } }).catch(() => {});
    }
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
