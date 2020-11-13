import TeamTask from '@/models/teamTask';

class Team {
    constructor(obj, taskModels) {
        const { Name: name, TeamId: id } = obj;
        this.name = name;
        this.id = id;
        this.ip = '10.0.0.' + id; // TODO: make this configurable
        this.taskModels = taskModels;
        this.update(obj);
    }

    update(team) {
        if (team.teamId != this.id) return;
        this.score = team.totalPoints;
        this.attack = team.attackPoints;
        this.defense = team.lostDefensePoints;
        this.sla = team.serviceLevelAgreementPoints;

        this.tasks = team.serviceDetails.map(
            teamTask => new TeamTask(teamTask)
        );

        let taskIds = this.tasks.map(x => x.taskId);
        for (let task of this.taskModels) {
            if (!taskIds.includes(task.id)) {
                this.tasks.push(
                    new TeamTask({
                        ServiceId: task.id,
                        ServiceLevelAgreementPoints: 0,
                        AttackPoints: 0,
                        LostDefensePoints: 0,
                        message: '',
                    })
                );
            }
        }
        this.tasks.sort(TeamTask.comp);
    }

    static comp(A, B) {
        return B.score - A.score;
    }
}

export default Team;
