<template>
    <div
        :class="[
            'ner-input',
            { 'ner-input--focused': focus, 'ner-input--invalid': invalid },
        ]"
    >
        <input
            ref="input"
            :value="value"
            :type="type"
            class="ner-input__input"
            :name="name"
            :disabled="disabled"
            :placeholder="placeholder"
            autocomplete="off"
            @input="handleInput"
            @change="handleChange"
        />
        <!-- <button
            v-if="showClearButton"
            type="button"
            class="icon-clear icon-button"
            @click="clearInput"
        >
            <ClearIcon />
        </button> -->
    </div>
</template>

<script>
// import ClearIcon from '../icons/ClearIcon';

export default {
    name: 'NerInput',
    // components: { ClearIcon },
    data() {
        return {
            value: '',
            showClearButton: false,
        };
    },
    props: {
        type: {
            type: String,
            default: 'text',
        },
        name: {
            type: String,
            default: '',
        },
        placeholder: {
            type: String,
            default: '',
        },
        disabled: [Boolean],
        clearable: {
            type: Boolean,
            default: false,
        },
    },
    watch: {
        focus() {
            if (this.focus) {
                this.$refs.input.focus();
            } else {
                this.$refs.input.blur();
            }
        },
    },
    methods: {
        handleInput(e) {
            this.showClearButton = e.target.value.length > 0 && this.clearable;
            this.$emit('on-input', e.target.value);
        },
        clearInput() {
            this.value = '';
            this.$emit('on-input', '');
        },
    },
};
</script>

<style>
.ner-input {
    position: relative;
    width: 100%;
}

.ner-input__input {
    margin: 0;
    width: 100%;
    box-sizing: border-box;
    background: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 6px;
    color: #333;
    transition: border-color 0.2s;
    font-family: inherit;
}

.ner-input__input::placeholder {
    color: rgba(136, 136, 136, 0.6);
}

.ner-input__input::-ms-clear {
    display: none;
}

.ner-input__input:disabled {
    background: #f1f4f5;
    border-color: #b7c0c4;
    cursor: auto;
}

.ner-input:hover .ner-input__input:not(:disabled) {
    border-color: #7e8f97;
}

.ner-input--focused .ner-input__input:not(:disabled),
.ner-input__input:active:not(:disabled),
.ner-input__input:focus:not(:disabled) {
    outline: 0;
    border-color: #79838a;
    box-shadow: 0 0 7px rgba(138, 149, 155, 0.2);
}

.ner-input--invalid .ner-input__input,
.ner-input--invalid:hover .ner-input__input:not(:disabled),
.ner-input--invalid .ner-input__input:active:not(:disabled),
.ner-input--invalid .ner-input__input:focus:not(:disabled) {
    outline: none;
    border-color: #eb5757;
    box-shadow: none;
}

.ner-input .icon-button {
    background-color: transparent;
    border: none;
    margin: 0;
    padding: 0;
}

.ner-input .icon-button:hover {
    cursor: pointer;
}

.ner-input .icon-button:focus,
.ner-input .icon-button:active {
    outline: none;
}

.ner-input .icon-clear {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    line-height: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}

.ner-input .ner-input__input {
    font-size: 14px;
    padding: 12px;
}

.ner-input .icon-clear {
    width: 16px;
    height: 16px;
    font-size: 11px;
    right: 14px;
}
</style>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type='number'] {
    -moz-appearance: textfield;
}
</style>
