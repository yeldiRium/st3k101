<template>
    <modal name="modal-create-question"
           height="auto"
           @before-open="beforeOpen"
    >
        <CreateResource
                @cancel="cancel"
                @create="create"
        >
            <template slot="header">
                Create new Question
            </template>
            <template slot="body">
                <input class="modal-create-question__question-text"
                       name="question-text"
                       v-model="text"
                />
                <RangeEditor :range="range"/>
            </template>
        </CreateResource>
    </modal>
</template>

<script>
    import {mapState} from "vuex";

    import {Language, LanguageData} from "../../../model/Language";
    import {Range} from "../../../model/SurveyBase/Config/Range";
    import {ConcreteQuestion} from "../../../model/SurveyBase/Question";

    import CreateResource from "./CreateResource";
    import RangeEditor from "../SurveyBase/Config/RangeEditor";

    export default {
        name: "ModalCreateQuestion",
        components: {
            CreateResource,
            RangeEditor
        },
        props: {
            /** @type {Language} */
            language: {
                type: Language
            }
        },
        data() {
            return {
                text: "Question text",
                range: null
            }
        },
        methods: {
            beforeOpen() {
                this.range = new Range({end: 10});
            },
            cancel() {
                this.$modal.hide("modal-create-question");
            },
            /**
             * Emits a "question-create" event with all data needed to create a
             * new Question.
             */
            create() {
                this.$emit("question-create", {
                    text: this.text,
                    range: this.range
                });
                this.$modal.hide("modal-create-question");
            }
        }
    }
</script>

<style lang="scss">
    .modal-create-question {
        &__question-text {
            width: 80%;
        }
    }
</style>
