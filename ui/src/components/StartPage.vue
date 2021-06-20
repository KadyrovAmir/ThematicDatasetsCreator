<template>
    <div class="ner-annotator">
        <div class="ner-annotator__body">
            <div class="ner-annotator__body-element">
                <div class="ner-annotator__subtitle">
                    <Training />
                    <span>
                        Разметка текста
                    </span>
                </div>
                <section class="ner-annotator__block">
                    <div class="ner-annotator__inner ner-annotator__inner-select">
                        <div class="ner-annotator__inner-title">
                            Выберите тему
                        </div>
                        <NerSelect
                            :options="options"
                            @on-select="onSelectTheme"
                        ></NerSelect>
                    </div>
                    <div class="ner-annotator__inner ner-annotator__inner-load">
                        <UploadFile @file-loaded="onFileLoadedMain" />
                    </div>
                </section>
                <section class="ner-annotator__title-confirm">
                    <NerButton @on-click="onConfirm" :disabled="!mainFile">
                        Начать разметку
                        <Loader v-if="isTagging" class="ner-annotator__loader-icon" />
                    </NerButton>
                </section>
            </div>
            <div class="ner-annotator__body-element">
                <div class="ner-annotator__subtitle">
                    <UpTraining />
                    <span>
                        Дообучение модели
                    </span>
                </div>
                <section class="ner-annotator__block">
                    <div class="ner-annotator__inner ner-annotator__inner-load">
                        <UploadFile @file-loaded="onFileLoadedTrain" fileType="json" />
                    </div>
                </section>
                <section v-if="!modelIsTraining" class="ner-annotator__title-confirm">
                    <NerButton @on-click="onUptrainModel" :disabled="!trainFile">
                        Дообучить модель
                    </NerButton>
                </section>
                <section class="ner-annotator__loader" v-else>
                    <span class="ner-annotator__loader-title">
                        Модель дообучается
                    </span>
                    <Loader />
                </section>
            </div>
            <div class="ner-annotator__body-element">
                <div class="ner-annotator__subtitle">
                    <UploadData />
                    <span>
                        Извлечение данных
                    </span>
                </div>
                <section class="ner-annotator__block">
                    <div class="ner-annotator__inner ner-annotator__inner-load">
                        <div class="ner-annotator__inner-title">
                            Впишите корректный url
                        </div>
                        <NerInput clearable placeholder="url" @on-input="handleInput" />
                    </div>
                </section>
                <section v-if="!isInceptionGoing" class="ner-annotator__title-confirm">
                    <NerButton @click="onInceptionData" :disabled="url.length === 0">
                        Извлечь данные
                    </NerButton>
                </section>
                <section class="ner-annotator__loader" v-else>
                    <span class="ner-annotator__loader-title">
                        Идет сбор датасетов с
                        <span class="ner-annotator__loader-url">{{ confirmedUrl }}</span
                        >. Это займёт некоторое время
                    </span>
                    <Loader />
                </section>
            </div>
        </div>
        <NerModal :show="showModal" @close="showModal = false">{{ modalText }}</NerModal>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import axios from '../axios';
import UploadFile from './UploadFile';
import NerSelect from './common/NerSelect.vue';
import NerInput from './common/NerInput.vue';
import NerButton from './common/NerButton.vue';
import TokenManager from './token-manager';
import UpTraining from './icons/UpTraining';
import Training from './icons/Training';
import Loader from './icons/Loader';
import UploadData from './icons/UploadData';
import { mapMutations } from 'vuex';

export default {
    name: 'StartPage',
    emits: ['file-loaded'],
    data() {
        return {
            options: [],
            fileData: '',
            tm: new TokenManager([]),
            mainFile: null,
            trainFile: null,
            modelIsTraining: false,
            isInceptionGoing: false,
            url: '',
            confirmedUrl: '',
            isTagging: false,
            showModal: false,
            modalText: '',
        };
    },
    components: {
        NerSelect,
        NerInput,
        NerButton,
        UploadFile,
        Training,
        UpTraining,
        Loader,
        UploadData,
    },
    mounted() {
        this.getThemes();
    },
    computed: {
        ...mapState(['selectedTheme']),
    },
    methods: {
        ...mapMutations(['setInputSentences', 'setTheme']),
        onFileLoadedMain(data) {
            this.setInputSentences(data);
            this.mainFile = data;
        },
        onFileLoadedTrain(data) {
            this.trainFile = data;
        },
        onConfirm() {
            this.isTagging = true;
            axios
                .post('/classes/' + this.selectedTheme, { text: this.mainFile })
                .then((res) => {
                    this.$emit('on-start', res);
                    res.data.classes.forEach((className) => {
                        this.$store.commit('addClass', className);
                    });

                    this.$store.commit('setTokens', res.data.annotations[1].entities);
                    this.isTagging = false;
                })
                .catch((err) => {
                    this.modalText = err;
                    this.showModal = true;
                });
        },
        onUptrainModel() {
            axios
                .post('/train', { data: JSON.parse(this.trainFile) })
                .then((res) => {
                    if (res.data.started) {
                        this.modelIsTraining = true;
                    }
                })
                .catch((err) => {
                    this.modalText = err;
                    this.showModal = true;
                });
        },
        onSelectTheme(data) {
            this.setTheme(data);
        },
        onInceptionData() {
            axios
                .post('/parse', { domain: this.url })
                .then((res) => {
                    if (res.data.started) {
                        this.confirmedUrl = this.url;
                        this.isInceptionGoing = true;
                    }
                })
                .catch((err) => {
                    this.modalText = err;
                    this.showModal = true;
                });
        },
        handleInput(data) {
            this.url = data;
        },
        getThemes() {
            axios
                .get('/themes')
                .then((res) => {
                    this.options = res.data.data;
                    this.setTheme(res.data.data[0].id);
                })
                .catch((err) => {
                    this.modalText = err;
                    this.showModal = true;
                });
        },
    },
};
</script>

<style scoped>
.ner-annotator {
    width: 100%;
    height: 100%;
    padding-top: 80px;
}

.ner-annotator__body {
    padding: 20px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

.ner-annotator__body-element {
    margin: 20px 20px 40px 20px;
    padding: 20px;
    border-radius: 20px;
    -webkit-box-shadow: 7px 6px 26px -5px rgba(34, 60, 80, 0.2);
    -moz-box-shadow: 7px 6px 26px -5px rgba(34, 60, 80, 0.2);
    box-shadow: 7px 6px 26px -5px rgba(34, 60, 80, 0.2);
}

.ner-annotator__body-element:hover {
    transition: 0.2s;
    transform: scale(1.008);
    -webkit-box-shadow: 7px 6px 26px 16px rgba(34, 60, 80, 0.2);
    -moz-box-shadow: 7px 6px 26px 16px rgba(34, 60, 80, 0.2);
    box-shadow: 7px 6px 26px 16px rgba(34, 60, 80, 0.2);
}

.ner-annotator__subtitle {
    font-size: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
}

.ner-annotator__subtitle svg {
    width: 20px;
    height: 20px;
    margin-right: 10px;
}

.ner-annotator__block {
    display: flex;
    justify-content: center;
}

.ner-annotator__inner {
    width: 100%;
    max-width: 400px;
    padding: 20px;
}

.ner-annotator__inner-title {
    font-size: 18px;
    padding-bottom: 10px;
    display: flex;
    justify-content: center;
    font-weight: bold;
}

.ner-annotator__title-confirm {
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ner-annotator__loader {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
    font-size: 18px;
}

.ner-annotator__loader-title {
    margin-right: 8px;
}

.ner-annotator__loader-icon {
    margin-left: 8px;
}

.ner-annotator__loader-url {
    color: #7905ff;
}
</style>
