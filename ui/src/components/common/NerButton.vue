<template>
    <button class="ner-button" :disabled="disabled" @click="$emit('on-click')">
        <slot />
    </button>
</template>

<script>
export default {
    name: 'NerButton',
    props: {
        disabled: [Boolean],
    },
};
</script>

<style>
.ner-button {
    display: inline-flex;
    justify-content: center;
    border-radius: 6px;
    font-weight: bold;
    text-decoration: none;
    cursor: pointer;
    padding: 10px 16px;
    font-size: 16px;
    line-height: 16px;
}

.ner-button:focus {
    outline: 0;
}

.ner-button {
    background: #ffffff;
    border: 1px solid #929292;
    color: #21323d;
}

.ner-button:hover {
    background: rgb(247, 247, 247);
    border-color: #747474;
}

.ner-button:active {
    background: rgb(238, 238, 238);
    border-color: #5e5e5e;
}

.ner-button:disabled {
    background: #ffffff;
    border-color: #d8e4ea;
    color: rgba(51, 51, 51, 0.3);
    cursor: auto;
    pointer-events: none;
    opacity: 0.6;
}
</style>
