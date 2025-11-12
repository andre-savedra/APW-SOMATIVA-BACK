import type { Movie } from "@/models/movies";
import { getAxios } from "./services.config";

export const getMovies = (): Promise<Array<Movie>>=>{
    return getAxios().get('/api/movies/');
}