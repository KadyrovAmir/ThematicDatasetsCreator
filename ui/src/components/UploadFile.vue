<template>
    <div>
        <div class="file-choose">
            Выберите файл
        </div>
        <div class="file-container">
            <div class="ner-load-file">
                <div class="file is-centered is-primary has-name is-boxed">
                    <label class="file-label">
                        <input
                            class="file-input"
                            type="file"
                            :name="`${fileType}file`"
                            :accept="`.${fileType}`"
                            @change="onFileSelected"
                        />
                        <span class="ner-load-file__button">
                            <span class="ner-load-file__button-text">
                                Нажмите тут
                            </span>
                            <File />
                        </span>
                    </label>
                </div>
            </div>
            <div v-if="fileName" class="current-file">
                <FileUploaded />
                <span class="current-file-name">{{ fileName }}</span> был успешно
                загружен!
            </div>
        </div>
    </div>
</template>

<script>
import { mapMutations } from 'vuex';
import File from './icons/File';
import FileUploaded from './icons/FileUploaded';

export default {
    name: 'UploadFile',
    components: {
        File,
        FileUploaded,
    },
    props: {
        fileType: {
            type: String,
            default: 'txt',
        },
    },
    data() {
        return {
            fileName: null,
        };
    },
    methods: {
        ...mapMutations(['setInputSentences']),
        onFileSelected(e) {
            let files = e.target.files;
            if (!files.length) return;

            let reader = new FileReader();
            reader.addEventListener('load', (event) => {
                this.$emit('file-loaded', event.target.result);
            });
            reader.readAsText(files[0]);
            this.fileName = files[0].name;
        },
    },
};
</script>

<style scoped>
.file-choose {
    font-size: 18px;
    padding-bottom: 10px;
    display: flex;
    justify-content: center;
    font-weight: bold;
}

.file-label {
    width: 200px;
}

.file-input {
    cursor: pointer;
}

.file-icon {
    width: 50%;
}

.ner-load-file {
    cursor: pointer;
}

.file-label {
    width: 100%;
    max-width: 350px;
}

.ner-load-file__button {
    background: #ffffff;
    border: 1px solid #cccccc;
    color: #21323d;

    padding: 10px;
    height: 40px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ner-load-file__button-text {
    margin-right: 10px;
}

.current-file {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
}

.current-file svg {
    margin-right: 6px;
}

.current-file-name {
    margin-right: 5px;
    color: #7905ff;
}
</style>
