<script setup lang="ts">
import { ref, type Ref } from 'vue';
import type { Movie } from './models/movies';
import { getMovies } from './services/movie.services';

const allMovies: Ref<Array<Movie>> = ref([]);

getMovies()
  .then(response=>allMovies.value = response)
  .catch(error=>console.error("Error when getting movies: ", error))

</script>

<template>
  <h1>Manflix</h1>
  <p>
    Lista de Filmes:
  </p>
    <table>
      <thead>
        <tr>
          <th>Id</th>
          <th>Título</th>
          <th>Descrição</th>
          <th>Categoria</th>
          <th>Data de publicação</th>
          <th>Foto</th>
          <th>Classificação</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(movie,id) in allMovies" :key="id">
          <td>{{movie.id}}</td>
          <td>{{movie.title}}</td>
          <td>{{movie.description}}</td>
          <td>{{movie.category}}</td>
          <td>{{movie.published_date}}</td>
          <td>
            <img class="movie-image" :src="movie.photo" alt="Foto do filme">
          </td>
          <td>{{movie.classification}}</td>
        </tr>
      </tbody>
    </table>
</template>

<style scoped lang="scss">
  .movie-image{
    height: 130px;
    width: auto;
    max-height: 200px;
  }
</style>
