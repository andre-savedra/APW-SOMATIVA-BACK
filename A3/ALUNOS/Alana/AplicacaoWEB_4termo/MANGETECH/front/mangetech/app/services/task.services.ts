import type { Page } from "~/models/page.model";
import type { Task } from "~/models/task.model";

export const getTasks = ()=>{
    return useFetch<Page<Task>>("http://localhost:8001/api/task/");
}

export const getTaskById = (id:string)=>{
    return useFetch<Task>(`http://localhost:8001/api/task/${id}/`);
}