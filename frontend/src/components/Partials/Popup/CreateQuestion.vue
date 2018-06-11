<template>
    <modal name="create-question">
        <CreateResource
                @cancel="cancel"
                @create="create"
        >
            <template slot="header">
                Create new Question
            </template>
            <template slot="body">
                <input class="popup-createquestion-questiontext"
                       name="questiontext"
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
        name: "Popup-CreateQuestion",
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
                range: new Range({end: 10})
            }
        },
        computed: {
            ...mapState("session", ["dataClient"])
        },
        methods: {
            cancel() {
                this.$modal.hide("create-question");
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

                console.log(question);

                this.$emit("question-created", question);
                this.$modal.hide("create-question");
            }
        }
    }
</script>

<style lang="scss">
    .popup-createquestion {
        &-text {
            width: 80%;
        }
    }
</style>
