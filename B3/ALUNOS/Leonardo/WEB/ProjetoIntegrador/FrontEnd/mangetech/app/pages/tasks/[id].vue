<script setup lang="ts">
const route = useRoute();
const { data: taskFound, error, pending } = 
    await useFetch(`http://localhost:8000/api/tasks/${route.params.id}/`)

</script>

<template>
    <h1>Tasks with id:         
        {{ taskFound }}
    </h1>
</template>