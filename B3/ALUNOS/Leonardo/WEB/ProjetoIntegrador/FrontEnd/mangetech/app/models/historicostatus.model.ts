import { STATUS } from "./enums.model";
import { User } from "./user.model";

export class HistoricoStatus {
    id: number = 0;
    tarefa: string = "";
    status_anterior: STATUS = STATUS.OPEN;
    novo_status: STATUS = STATUS.INPROCESS;
    descricao: string = "";
    data_alteracao: Date = new Date();
    alterado_por: User = new User();
}