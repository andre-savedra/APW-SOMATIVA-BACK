<script setup lang="ts">
import { getTasks } from '~/services/task.services';

const { data: allTasks } = await getTasks();

</script>

<template>
    <h1>Tasks Page!</h1>    
    <table>
        <thead>
            <th>ID Chamado</th>
            <th>Solicitante</th>
            <th>Título</th>
            <th>Descrição</th>
            <th>Data de Abertura</th>
            <th>Urgência</th>
        </thead>
        <tbody>
            <tr v-for="(task, index) in allTasks?.results" :key="index">
                <td>{{ task.id }}</td>
                <td>{{ task.creator_FK.name }}</td>
                <td>{{ task.name }}</td>
                <td>{{ task.description }}</td>
                <td>{{ task.creation_date }}</td>
                <td>{{ task.urgency_level }}</td>
            </tr>
        </tbody>

    </table>

</template>