<script setup lang="ts">
    //composable: função que aproveita a lógica em varias partes do nosso projeto
    const route = useRoute();

</script>



<template>
    <h1>Equipment with ID: {{ route.params.id }}</h1> <!--comocamos .id pq é o nome do arquivo-->
</template>