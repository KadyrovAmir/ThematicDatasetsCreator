<template>
    <transition name="modal" v-if="show" @click="$emit('close')">
        <div class="modal-mask">
            <div class="modal-wrapper">
                <div class="modal-container">
                    <div class="modal-body">
                        <slot>
                            default body
                        </slot>
                    </div>
                    <div class="modal-footer">
                        <NerButton class="modal-default-button" @click="$emit('close')">
                            Ок
                        </NerButton>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script>
import NerButton from './NerButton.vue';
export default {
    name: 'NerModal',
    components: { NerButton },
    props: {
        show: {
            type: Boolean,
            default: false,
        },
    },
};
</script>

<style scoped>
.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(1, 0, 0, 0.5);
    display: table;
    transition: opacity 1.3s ease;
}

.modal-wrapper {
    display: table-cell;
    vertical-align: middle;
}

.modal-container {
    width: 300px;
    margin: 0px auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
    font-family: Helvetica, Arial, sans-serif;
    min-height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.modal-body {
    margin: 10px 0;
}

.modal-default-button {
    float: right;
}
</style>
