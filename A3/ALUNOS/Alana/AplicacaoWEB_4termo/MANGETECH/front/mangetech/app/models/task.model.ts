import { URGENCY_LEVEL } from "./enums.model";
import type { Equipment } from "./equipment.model";
import { User } from "./user.model";

export class Task {
    id: number = 0;
    name: string = "";
    description: string = "";
    suggested_date: Date = new Date();
    urgency_level: URGENCY_LEVEL = URGENCY_LEVEL.LOW;
    creation_date: Date = new Date();
    creator_FK: User = new User();
    equipments_FK: Array<Equipment> = [];
    responsibles_FK: Array<User> = [];
}