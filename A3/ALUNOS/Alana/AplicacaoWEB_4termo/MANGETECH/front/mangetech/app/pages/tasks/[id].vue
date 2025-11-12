<script setup lang="ts">
import { Task } from '~/models/task.model';
import { getTaskById } from '~/services/task.services';

    const route = useRoute();
    const taskId = route.params.id ?? "";
    const task: Ref<Task> = ref(new Task());
    
    if(typeof(taskId) == 'string'){
        const { data: taskFound } = await getTaskById(taskId);      
        if(taskFound.value){
            task.value = taskFound.value;            
        }
    }
</script>

<template>
    <h1>Task with ID: {{ route.params.id }}</h1>
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
            <tr>
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