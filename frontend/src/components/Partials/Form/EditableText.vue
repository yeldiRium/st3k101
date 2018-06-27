<template>
    <div class="editable-text"
    >
        <div class="editable-text__form"
             v-if="editing"
             v-click-outside="cancelEditing"
        >
            <textarea v-if="textArea"
                      v-model="runningValue"
                      ref="input"
                      @keyup.esc="cancelEditing"
            />
            <input v-else
                   v-model="runningValue"
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
        >
            <span>
                {{ value }}
            </span>
            <IconEdit class="editable-text__edit-icon"
                      height="1em"
                      width="1em"
                      viewBox="0 0 24 24"
                      @click.native.prevent.stop="startEditing"
            />
        </div>
    </div>
</template>

<script>
    import IconEdit from "../../../assets/icons/baseline-edit-24px.svg";

    export default {
        name: "EditableText",
        components: {
            IconEdit
        },
        props: {
            value: {
                type: String
            },
            ellipseText: {
                type: Boolean,
                default: false
            },
            textArea: {
                type: Boolean,
                default: false
            }
        },
        data() {
            return {
                editing: false,
                storedValue: "",
                runningValue: ""
            };
        },
        watch: {
            value: {
                immediate: true,
                handler(value) {
                    this.runningValue = value;
                }
            }
        },
        methods: {
            startEditing() {
                this.editing = true;
                this.storedValue = this.runningValue;
                this.$nextTick(() => {
                    this.$refs.input.focus();
                })
            },
            finishEditing() {
                this.editing = false;
                this.$emit("input", this.runningValue);
            },
            cancelEditing() {
                this.editing = false;
                this.runningValue = this.storedValue;
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_mixins";

    .editable-text {
        &__text {
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 1em;

            &--ellipse {
                span {
                    @include ellipse();
                }
            }
        }

        &__form {
            width: 100%;
            display: grid;
            grid-auto-flow: column;
            grid-template-columns: auto 4em;
        }

        &__edit-icon {
            cursor: pointer;
            transform: scale(.8, .8);
            transform-origin: bottom left;
        }
    }
</style>
