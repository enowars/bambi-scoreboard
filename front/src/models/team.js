import TeamTask from '@/models/teamTask';

class Team {
    constructor({ name, ip, id, teamTasks, tasks, highlighted }) {
        this.name = name;
        this.ip = ip;
        this.id = id;
        this.highlighted = highlighted;
        this.taskModels = tasks;
        this.update(teamTasks);
    }

    update(teamTasks) {
        this.tasks = teamTasks
            .filter(({ team_id: teamId }) => teamId === this.id)
            .map(teamTask => new TeamTask(teamTask));
        this.score = this.tasks.reduce(
            (acc, { sla, attack, defense }) => acc + sla + attack + defense,
            0
        );
        let taskIds = this.tasks.map(x => x.taskId);
        for (let task of this.taskModels) {
            if (!taskIds.includes(task.id)) {
                console.log('Creating new task for ' + task.id);
                this.tasks.push(
                    new TeamTask({
                        id: 0,
                        task_id: task.id,
                        team_id: this.id,
                        sla: 0,
                        attack: 0,
                        defense: 0,
                        message: '',
                        status: 101,
                    })
                );
            }
        }
        this.tasks.sort(TeamTask.comp);
        console.log(this.tasks);
    }

    static comp(A, B) {
        return B.score - A.score;
    }
}

export default Team;
