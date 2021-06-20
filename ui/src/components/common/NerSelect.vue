<template>
    <div class="custom-select" :tabindex="tabindex" @blur="isOpen = false">
        <div class="selected" :class="{ open: isOpen }" @click="isOpen = !isOpen">
            <span>
                {{ selected }}
            </span>
        </div>
        <div class="items" :class="{ 'select-is-hidden': !isOpen }">
            <div
                v-for="(option, i) of options"
                :key="i"
                @click="onClickHandler(option)"
                :value="option.id"
            >
                {{ option.name }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        options: {
            type: Array,
            required: true,
        },
        tabindex: {
            type: Number,
            required: false,
            default: 0,
        },
    },
    data() {
        return {
            selected: this.options.length > 0 ? this.options[0].name : '-',
            isOpen: false,
        };
    },
    mounted() {},
    methods: {
        onClickHandler(option) {
            this.selected = option.name;
            this.isOpen = false;
            this.$emit('on-select', option.id);
        },
    },
};
</script>

<style scoped>
.custom-select {
    position: relative;
    width: 100%;
    text-align: left;
    outline: none;
    height: 40px;
    line-height: 40px;
}

.custom-select .selected {
    background: #ffffff;
    border: 1px solid #cccccc;
    color: #21323d;
    border-radius: 6px;
    padding-left: 1em;
    cursor: pointer;
    user-select: none;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    padding-right: 24px;
}

.custom-select .selected.open {
    border: 1px solid #cccccc;
    border-radius: 6px 6px 0px 0px;
}

.custom-select .selected:after {
    position: absolute;
    content: '';
    top: 22px;
    right: 1em;
    width: 0;
    height: 0;
    border: 5px solid transparent;
    border-color: rgb(0, 0, 0) transparent transparent transparent;
}

.custom-select .items {
    color: #222222;
    border-radius: 0px 0px 6px 6px;
    overflow: hidden;
    position: absolute;
    background-color: #fdfdfd;
    border: 1px solid #cccccc;
    left: 0;
    right: 0;
    z-index: 100;
    max-height: 220px;
    overflow-y: scroll;
}

.custom-select .items div {
    color: #2c2c2c;
    padding-left: 1em;
    cursor: pointer;
    user-select: none;
}

.custom-select .items div:hover {
    background-color: #f1f1f1;
}

.select-is-hidden {
    display: none;
}
</style>
