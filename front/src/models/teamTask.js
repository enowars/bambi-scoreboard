class TeamTask {
    constructor({
        ServiceId: taskId,
        ServiceStatus: status,
        ServiceLevelAgreementPoints: sla,
        AttackPoints: attack,
        LostDefensePoints: defense,
        Message: message,
    }) {
        this.id = taskId + sla * 100 + attack * 10000 + defense * 1000000;
        this.taskId = taskId;
        if (status === 'INACTIVE') {
            this.status = 111;
        } else if (status === 'OK') {
            this.status = 101;
        } else if (status === 'RECOVERING') {
            this.status = 102;
        } else if (status === 'MUMBLE') {
            this.status = 103;
        } else if (status === 'OFFLINE') {
            this.status = 104;
        } else {
            // INTERNAL_ERROR
            this.status = 110;
        }
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
