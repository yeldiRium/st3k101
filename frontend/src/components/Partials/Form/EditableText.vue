<template>
    <div class="editable-text"
    >
        <div class="editable-text__form"
             v-if="editing"
        >
            <input :value="text"
                   ref="input"
                   @keyup.enter="finishEditing"
                   @keyup.esc="cancelEditing"
            />
            <button @click="finishEditing">
                Ok
            </button>
        </div>
        <div class="editable-text__text"
             v-else
             @dblclick.prevent.stop="startEditing"
        >
            {{ text }}
        </div>
    </div>
</template>

<script>
    export default {
        name: "EditableText",
        props: {
            text: {
                type: String
            }
        },
        data() {
            return {
                editing: false,
                storedValue: ""
            };
        },
        methods: {
            handleInput(event) {
                this.$emit("edit", event);
            },
            startEditing() {
                this.editing = true;
                this.storedValue = this.text;
                this.$nextTick(() => {
                    this.$refs.input.focus();
                })
            },
            finishEditing() {
                this.editing = false;
                this.$emit("edit", this.$refs.input.value);
            },
            cancelEditing() {
                this.editing = false;
                this.$emit("edit", this.storedValue);
            }
        }
    }
</script>

<style lang="scss">
    .editable-text {
        &__text {
            cursor: pointer;
        }
    }
</style>
