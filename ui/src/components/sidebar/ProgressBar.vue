<template>
    <div class="progress-bar">
        <p><strong>Прогресс</strong></p>
        <p class="is-size-7 has-text-right">Завершено {{ completed }}/{{ total }}</p>
        <progress class="progress is-small is-primary" :value="completed" :max="total">
            {{ completedPercent }}%
        </progress>
    </div>
</template>

<script>
export default {
    name: 'ProgressBar',
    props: {
        completed: {
            type: Number,
            required: true,
        },
        total: {
            type: Number,
            required: true,
        },
    },
    computed: {
        completedPercent() {
            return parseInt((this.completed / this.total) * 100);
        },
    },
};
</script>

<style scoped>
.progress-bar {
    margin-top: 20px;
    max-width: 200px;
}
</style>
