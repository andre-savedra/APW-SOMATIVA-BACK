export class Director {
    name: string = "";
}

export class Movie {
    id: number = 0;
    title: string = "";
    description: string = "";
    category: string = "";
    published_date: Date = new Date();
    photo: string = "";
    classification: number = 0;
    directors: Array<Director> = [];    
}

