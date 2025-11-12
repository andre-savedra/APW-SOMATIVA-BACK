import { Ambiente } from "./ambiente.model";

export class Ativo {
    id: number = 0;
    name: string = "";
    number: string = "";
    description: string = "";
    creation_date: Date = new Date();
    category_FK: string = "";
    ambientes: Ambiente = new Ambiente();
}