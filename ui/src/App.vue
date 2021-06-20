<template>
    <div>
        <section class="ner-annotator__title">
            <span class="ner-annotator__title-text">Datasets Creator</span>
        </section>
        <StartPage v-if="currentPage === 'start'" @on-start="onStart" />
        <AnnotationPage v-else @on-back="onBack" :data="data" />
    </div>
</template>

<script>
import StartPage from './components/StartPage';
import AnnotationPage from './components/AnnotationPage';

import './assets/styles.scss';

export default {
    name: 'App',
    data: function() {
        return {
            currentPage: 'start',
            data: () => ({}),
        };
    },
    components: {
        StartPage,
        AnnotationPage,
    },
    methods: {
        onStart(data) {
            this.data = data;
            this.currentPage = 'annotator';
        },
        onBack() {
            this.currentPage = 'start';
        },
    },
};
</script>

<style scoped>
.ner-annotator__title {
    background-color: #ffffff;
    padding: 20px;
    display: flex;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 10000;
    -webkit-box-shadow: 0px 5px 5px 5px rgba(34, 60, 80, 0.6);
    -moz-box-shadow: 0px 5px 5px -5px rgba(34, 60, 80, 0.6);
    box-shadow: 0px 5px 5px -5px rgba(34, 60, 80, 0.6);
}

.ner-annotator__title-text {
    color: #3a3a3a;
    font-size: 30px;
    font-weight: bold;
}
</style>
