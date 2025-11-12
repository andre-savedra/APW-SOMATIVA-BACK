export class Page<T> {
    count: number = 0;
    next: string|null = null;
    previous: string|null = null;
    results: Array<T> = [];
}