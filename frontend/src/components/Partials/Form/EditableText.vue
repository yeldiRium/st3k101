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
             :class="{'editable-text__text--ellipse': ellipseText}"
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
            },
            ellipseText: {
                type: Boolean,
                default: false
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
    @import "../../scss/_mixins";

    .editable-text {
        &__text {
            cursor: pointer;

            &--ellipse {
                @include ellipse();
            }
        }
    }
</style>
