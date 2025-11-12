import { Category } from "./category.model";
import { Environment } from "./environment.model";

export class Equipment {
    id: number = 0;
    name: string = "";
    code: string = "";
    description: string = "";
    creation_date: Date = new Date();
    category_FK: Category = new Category();
    environment_FK: Environment = new Environment();
}