class TeamTask {
    constructor({
        id,
        round,
        task_id: taskId,
        team_id: teamId,
        status,
        sla,
        attack,
        defense,
        message,
    }) {
        this.id = id;
        (this.round = round), (this.taskId = taskId);
        this.teamId = teamId;
        this.status = status;
        this.sla = sla;
        this.attack = attack;
        this.defense = defense;
        this.message = message;
    }

    static comp(A, B) {
        return A.taskId - B.taskId;
    }
}

export default TeamTask;
