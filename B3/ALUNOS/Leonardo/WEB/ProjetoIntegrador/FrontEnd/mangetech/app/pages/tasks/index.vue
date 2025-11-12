<script setup lang="ts">
const { data: tasksFound, error, pending } = 
    await useFetch("http://localhost:8000/api/tasks/")

</script>


<template>
    <h1>Tasks Page</h1>
    <p>{{ tasksFound }}</p>
</template>