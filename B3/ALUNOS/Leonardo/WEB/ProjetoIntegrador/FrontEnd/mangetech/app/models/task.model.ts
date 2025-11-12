import { URGENCY_LEVELS } from "./enums.model";
import { STATUS } from "./enums.model";
import type { Ativo } from "./ativo.model";
import { User } from "./user.model";

export class Tarefas {
    id: number = 0;
    name: string = "";
    description: string = "";
    status: STATUS = STATUS.OPEN;
    start_date_status: Date = new Date();
    suggested_date: Date = new Date();
    resolution_date: Date = new Date();
    responsibles: User = new User();
    ativos: Array<Ativo> = [];
    urgency: URGENCY_LEVELS = URGENCY_LEVELS.LOW;
                                     
}
    
