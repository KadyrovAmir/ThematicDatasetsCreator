<template>
    <button class="button is-danger" @click="generateJSONExport">
        Экспорт аннотаций
    </button>
</template>

<script>
import axios from '../../axios';
import { mapState } from 'vuex';

export default {
    name: 'Export',
    computed: {
        ...mapState(['annotations', 'classes', 'selectedTheme']),
    },
    methods: {
        generateJSONExport() {
            const filename = 'training_data.json';
            const classes = this.classes.map(({ name }) => name);
            const output = {
                classes,
                annotations: this.annotations,
            };
            const jsonStr = JSON.stringify(output);

            let element = document.createElement('a');
            element.setAttribute(
                'href',
                'data:text/plain;charset=utf-8,' + encodeURIComponent(jsonStr)
            );
            element.setAttribute('download', filename);

            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);

            axios
                .post('/classes/' + this.selectedTheme + '/update-classes', {
                    classes,
                })
                .then(() => {})
                .catch((err) => alert(err));
        },
    },
};
</script>
