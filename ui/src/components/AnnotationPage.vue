<template>
    <div class="ner-annotator__tokens columns is-desktop">
        <div class="left-column">
            <AnnotationSidebar :current="currentSentence" @on-back="$emit('on-back')" />
        </div>
        <div class="right-column">
            <div class="panel">
                <div class="panel-heading">
                    <classes-block />
                </div>
                <div class="panel-block">
                    <div id="editor">
                        <component
                            :is="t.type === 'token' ? 'Token' : 'TokenBlock'"
                            :id="'t' + t.start"
                            v-for="t in tm.tokens"
                            :token="t"
                            :key="t.start"
                            :backgroundColor="t.backgroundColor"
                            @remove-block="onRemoveBlock"
                        />
                    </div>
                </div>
                <div class="panel-block">
                    <div class="button-group">
                        <p class="control">
                            <button
                                class="button is-danger is-outlined"
                                @click="resetBlocks"
                            >
                                Сбросить
                            </button>
                        </p>
                        <p class="control">
                            <button class="button" @click="skipCurrentSentence">
                                Пропустить
                            </button>
                        </p>
                        <p class="control">
                            <button class="button is-link" @click="saveTags">
                                Сохранить
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <NerModal :show="showModal" @close="showModal = false">{{ modalText }}</NerModal>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import axios from '../axios';
import Token from './Token';
import TokenBlock from './TokenBlock';
import AnnotationSidebar from './AnnotationSidebar';
import ClassesBlock from './ClassesBlock.vue';
import TokenManager from './token-manager';
import NerModal from '../components/common/NerModal';

export default {
    name: 'AnnotationPage',
    data: function() {
        return {
            tm: new TokenManager([]),
            currentSentence: {},
            currentIndex: 0,
            redone: '',
            showModal: false,
            modalText: '',
        };
    },
    components: {
        Token,
        TokenBlock,
        AnnotationSidebar,
        ClassesBlock,
        NerModal,
    },
    computed: {
        ...mapState([
            'inputSentences',
            'classes',
            'annotations',
            'currentClass',
            'defaultTokens',
        ]),
    },
    watch: {
        inputSentences() {
            this.currentIndex = 0;
            this.tokenizeCurrentSentence();
        },
    },
    created() {
        if (this.inputSentences.length) {
            this.tokenizeCurrentSentence();
        }
        document.addEventListener('mouseup', this.selectTokens);
    },
    beforeUnmount() {
        document.removeEventListener('mouseup', this.selectTokens);
    },
    methods: {
        tokenizeCurrentSentence() {
            if (this.currentIndex >= this.inputSentences.length) {
                this.modalText = 'Разметка завершена';
                this.showModal = true;
                return;
            }
            this.currentSentence = this.inputSentences[this.currentIndex];
            axios
                .post('/tokenize', this.currentSentence)
                .then((res) => {
                    this.tm = new TokenManager(res.data.tokens);
                    this.defaultTokens.forEach(([startIdx, endIdx, currentClass]) => {
                        const classObject = this.classes.find(
                            ({ name }) => name === currentClass
                        );
                        this.tm.addNewBlock(startIdx, endIdx, classObject);
                    });
                })
                .catch((err) => {
                    this.modalText = err;
                    this.showModal = true;
                });
        },
        selectTokens() {
            let selection = document.getSelection();

            if (
                selection.anchorOffset === selection.focusOffset &&
                selection.anchorNode === selection.focusNode
            )
                return;
            let startIdx, endIdx;
            try {
                startIdx = parseInt(
                    selection.anchorNode.parentElement.id.replace('t', '')
                );
                endIdx = parseInt(selection.focusNode.parentElement.id.replace('t', ''));
            } catch (e) {
                console.log('selected text were not tokens');
                return;
            }

            if (!this.classes.length && selection.anchorNode) {
                this.modalText =
                    'Нет доступных тегов. Добавьте несколько тегов перед разметкой';
                this.showModal = true;
                selection.empty();
                return;
            }

            this.tm.addNewBlock(startIdx, endIdx, this.currentClass);
            selection.empty();
        },
        onRemoveBlock(blockStart) {
            this.tm.removeBlock(blockStart);
        },
        resetBlocks() {
            this.tm.resetBlocks();
        },
        skipCurrentSentence() {
            this.currentIndex++;
            this.tokenizeCurrentSentence();
        },
        saveTags() {
            axios
                .post('/detokenize', { tokens: this.tm.words })
                .then((res) => {
                    this.$store.commit('addAnnotation', [
                        res.data.text,
                        { entities: this.tm.exportAsAnnotation() },
                    ]);
                    this.currentIndex++;
                    this.tokenizeCurrentSentence();
                })
                .catch((e) => {
                    console.log(e);
                });
        },
    },
};
</script>

<style scoped>
#editor {
    padding: 20px;
}
.ner-annotator__tokens {
    padding-top: 100px;
}

.left-column {
    display: block;
    flex-basis: 0;
    flex-grow: 1;
    flex-shrink: 1;
    margin: 20px 10px 20px 30px;
}

.panel-block {
    padding: 0;
}

.right-column {
    flex-grow: 3;
    margin: 20px 30px 20px 10px;
}

.button-group {
    display: flex;
    align-items: center;
    justify-content: start;
    padding: 15px 20px;
}

.button-group .control {
    margin-right: 10px;
}
</style>
