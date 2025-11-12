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
  <h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>
  <p>{{ allMovies }}</p>
</template>

<style scoped></style>
