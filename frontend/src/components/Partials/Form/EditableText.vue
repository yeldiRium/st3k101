<template>
    <div class="editabletext"
    >
        <div class="editabletext-form"
             v-if="editing"
        >
            <input :value="value"
                   ref="input"
                   @keyup.enter="finishEditing"
                   @keyup.esc="cancelEditing"
            />
            <button @click="finishEditing">
                Ok
            </button>
        </div>
        <div class="editabletext-text"
             v-else
             @dblclick.prevent.stop="startEditing"
        >
            {{ value }}
        </div>
    </div>
</template>

<script>
    export default {
        name: "EditableText",
        props: {
            value: {
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
                console.log(event);
                this.$emit("input", event);
            },
            startEditing() {
                this.editing = true;
                this.storedValue = this.value;
                this.$nextTick(() => {
                    this.$refs.input.focus();
                })
            },
            finishEditing() {
                this.editing = false;
                console.log(this.$refs);
                this.$emit("input", this.$refs.input.value);
            },
            cancelEditing() {
                this.editing = false;
                this.$emit("input", this.storedValue);
            }
        }
    }
</script>

<style lang="scss">

</style>
