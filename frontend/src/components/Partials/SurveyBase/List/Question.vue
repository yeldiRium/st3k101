<template>
    <ListItem class="list-question"
              v-bind="$attrs"
              v-on="$listeners"
              :text="question.text"
              :mini="true"
              :disabled="!isEditable(question)"
              @edit="updateQuestionText"
    >
        <slot></slot>
        <LanguagePicker class="list-item__language-picker"
                        :language-data="question.languageData"
                        @choose-language="changeLanguage"
                        @choose-language-unavailable="addNewTranslation"
        />
        <IconReorder class="list-item__icon"
                     v-if="draggable"
        />
    </ListItem>
</template>

<script>
    import QuestionBase from "../QuestionBase";
    import ListItem from "../../List/Item";
    import LanguagePicker from "../../LanguagePicker";

    import IconEdit from "../../../../assets/icons/baseline-edit-24px.svg";
    import IconReorder from "../../../../assets/icons/baseline-reorder-24px.svg";

    import {fetchTranslation, setText} from "../../../../api2/Question";

    /**
     * Displays a Question as a ListElement.
     *
     * Does not display all the Question's state because of space reasons. To
     * display all Question state use the Full/Question component.
     *
     * The Question will be uneditable (text can't be changed), if it is a Sha-
     * dowQuestion or not owned by the current DataClient.
     */
    export default {
        name: "ListQuestion",
        extends: QuestionBase,
        components: {
            ListItem,
            LanguagePicker,
            IconEdit,
            IconReorder
        },
        methods: {
            /**
             * Switch the Question to the given language.
             * @param {Language} language
             */
            changeLanguage(language) {
                fetchTranslation(this.question, language);
            },
            /**
             * Add a new translation to the Question.
             * This means set new field values via API for the given languages
             * and then fetch the question anew in the now existing language.
             * @param language
             */
            addNewTranslation(language) {
                // TODO: clarify, when this should be available
                // TODO: display dialog which asks for data
                const text = "tbd";
                setText(this.question, language, text);
                this.changeLanguage(language);
            },
            updateQuestionText(text) {
                if (!this.isEditable(this.question)) {
                    return;
                }
                setText(
                    this.question,
                    this.question.languageData.currentLanguage,
                    text
                );
            }
        }
    }
</script>

<style lang="scss">
    .list-question.list-item {
        min-height: 3em;

        &--mini {
            min-height: 2em;
        }
    }
</style>
