<template>
    <div>
        <NerButton class="back-button" @click="$emit('on-back')">
            Назад
        </NerButton>
        <div class="side-bar-nav">
            <SplitTypeSelector />
            <ProgressBar
                class="mb-5"
                :completed="current.id"
                :total="inputSentences.length"
            />
            <Export />
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import Export from './sidebar/Export.vue';
import ProgressBar from './sidebar/ProgressBar.vue';
import SplitTypeSelector from './sidebar/SplitTypeSelector.vue';
import NerButton from './../components/common/NerButton';

export default {
    name: 'AnnotationSidebar',
    props: {
        current: {
            type: Object,
            required: true,
        },
    },
    components: {
        ProgressBar,
        Export,
        SplitTypeSelector,
        NerButton,
    },
    computed: {
        ...mapState(['inputSentences']),
        visibleSentences() {
            let start = this.current.id;
            if (start + 10 > this.inputSentences.length) {
                start = this.inputSentences.length - 10;
            }
            let end = start + 10;
            return this.inputSentences.slice(start, end);
        },
    },
};
</script>

<style lang="scss">
.is-single-line {
    width: 90%;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}
</style>

<style scoped>
.side-bar-nav {
    width: 100%;
}
</style>
