<template>
    <div class="field is-grouped is-grouped-multiline">
        <div class="control" v-for="cl in classes" :key="cl.id">
            <div class="tags is-medium has-addons">
                <a
                    class="tag is-medium"
                    :class="{ 'is-link': cl.id === currentClass.id }"
                    @click="setCurrentClass(cl.id)"
                >
                    <span class="color-box" :style="{ backgroundColor: cl.color }"></span>
                    {{ cl.name }}
                </a>
                <a class="tag is-medium is-delete" @click="removeClass(cl.id)"></a>
            </div>
        </div>

        <div class="control">
            <input
                type="text"
                class="input"
                v-model="newClassName"
                @keyup="onInputKeyup"
                placeholder="Новый тэг"
            />
            <button class="button is-info is-inline" @click="saveNewClass">
                Добавить
            </button>
        </div>
    </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
export default {
    name: 'ClassesBlock',
    data() {
        return {
            showNewClassInput: false,
            newClassName: '',
        };
    },
    computed: {
        ...mapState(['classes', 'currentClass']),
    },
    watch: {
        newClassName(now, then) {
            if (now != then) {
                this.newClassName = now.toUpperCase();
            }
        },
    },
    methods: {
        ...mapMutations(['removeClass', 'setCurrentClass']),
        saveNewClass() {
            this.$store.commit('addClass', this.newClassName);
            this.showNewClassInput = false;
            this.newClassName = '';
        },
        onInputKeyup(e) {
            if (e.key === 'Enter') {
                this.saveNewClass();
            }
        },
    },
};
</script>

<style scoped>
.color-box {
    width: 1rem;
    height: 1rem;
    margin-right: 1rem;
}

.input {
    width: 250px;
    margin-right: 8px;
}
</style>
