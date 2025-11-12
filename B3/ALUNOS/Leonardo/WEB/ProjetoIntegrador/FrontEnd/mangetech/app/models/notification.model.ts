import { Tarefas } from "./task.model";
import { User } from "./user.model";

export class Notification {
    id: number = 0;
    text: string = "";
    task_FK: Tarefas = new Tarefas();
    user_FK: User = new User();
    creation_date: Date = new Date();
    read: boolean = false;
}