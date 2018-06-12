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
        computed: {
            ...mapState("session", ["dataClient"])
        },
        methods: {
            beforeOpen() {
                this.range = new Range({end: 10});
            },
            cancel() {
                this.$modal.hide("modal-create-question");
            },
            /**
             * Creates the question and emits it via a "question-created" event.
             * TODO: send API request with all data, then set href and owner to
             *       the returned values
             *       Also refactor this in general. This is currently as demon-
             *       strative of intent as possible and should be improved upon.
             */
            create() {
                const href = "someshittyhref" + String(Math.random());
                const owner = this.dataClient;
                const languageData = new LanguageData(
                    this.language,
                    this.language,
                    [this.language]
                );
                const text = this.text;
                const range = this.range;
                const incomingReferenceCount = 0;
                const ownedIncomingReferences = [];

                const question = new ConcreteQuestion(
                    href,
                    owner,
                    languageData,
                    text,
                    range,
                    incomingReferenceCount,
                    ownedIncomingReferences
                );

                this.$emit("question-created", question);
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
