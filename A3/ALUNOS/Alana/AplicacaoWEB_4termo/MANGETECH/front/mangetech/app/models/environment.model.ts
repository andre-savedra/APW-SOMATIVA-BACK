import { User } from "./user.model";

export class Environment {
    id: number = 0;
    name: string = "";
    user_FK: User = new User();
}