<template>
    <ListItem class="list-questionnaire"
              v-bind="$attrs"
              v-on="$listeners"
              :text="questionnaire.name"
              :subtext="subtext"
              :mini="disableSubText"
              :disabled="!isEditable(questionnaire)"
              @edit="updateQuestionnaireName"
    >
        <slot></slot>
        <LanguagePicker class="list-item__language-picker"
                        :language-data="questionnaire.languageData"
                        @choose-language="changeLanguage"
                        @choose-language-unavailable="addNewTranslation"
        />
        <IconReorder class="list-item__icon"
                     v-if="draggable"
        />
    </ListItem>
</template>

<script>
    import {map, path, sum} from "ramda";

    import QuestionnaireBase from "../QuestionnaireBase";
    import ListItem from "../../List/Item";
    import LanguagePicker from "../../LanguagePicker";

    import IconEdit from "../../../../assets/icons/baseline-edit-24px.svg";
    import IconReorder from "../../../../assets/icons/baseline-reorder-24px.svg";

    /**
     * Displays a Questionnaire as a ListElement.
     *
     * Does not display all the Questionnaire's state because of space reasons. To
     * display all Questionnaire state use the FullQuestionnaire component.
     *
     * The Questionnaire will be uneditable, if it is a ShadowQuestionnaire or
     * not owned by the current DataClient.
     */
    export default {
        name: "ListQuestionnaire",
        extends: QuestionnaireBase,
        components: {
            ListItem,
            LanguagePicker,
            IconEdit,
            IconReorder
        },
        props: {
            disableSubText: {
                type: Boolean,
                default: false
            }
        },
        computed: {
            /**
             * Returns a message displaying the number of Dimensions and Ques-
             * tions in the Questionnaire.
             *
             * @returns {string}
             */
            subtext() {
                let questionCount = sum(
                    map(
                        path(["questions", "length"]),
                        this.questionnaire.dimensions
                    )
                );
                return `Contains ${this.questionnaire.dimensions.length} dimensions and ${questionCount} questions.`;
            }
        },
        methods: {
            /**
             * Switch the Questionnaire to the given language.
             * @param {Language} language
             */
            changeLanguage(language) {
                this.questionnaire.fetchTranslation(language);
            },
            /**
             * Add a new translation to the Questionnaire.
             * This means set new field values via API for the given langages
             * and then fetch the Questionnaire anew in the now existing langu-
             * age.
             * @param language
             */
            addNewTranslation(language) {
                // TODO: clarify, when this should be available
                // TODO: create new translation
                // this.questionnaire.fetchTranslation(language);
            },
            updateQuestionnaireName(name) {
                // TODO: set via API.
                this.questionnaire.name = name;
            }
        }
    }
</script>

<style lang="scss">
    .list-questionnaire.list-item {
        min-height: 3em;

        &--mini {
            min-height: 2em;
        }
    }
</style>
