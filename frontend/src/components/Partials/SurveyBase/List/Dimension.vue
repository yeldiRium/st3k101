<template>
    <ListItem class="list-dimension"
              v-bind="$attrs"
              v-on="$listeners"
              :text="dimension.name"
              :subtext="subtext"
              :mini="disableSubText"
              :disabled="disabled(dimension)"
              :icons="iconsNeeded(dimension)"
    >
        <slot></slot>
        <LanguagePicker class="list-item-languagepicker"
                        :language-data="dimension.languageData"
                        v-if="!disableLanguagePicker"
                        @choose-language="changeLanguage"
                        @choose-language-unavailable="addNewTranslation"
        />
        <IconReorder class="list-item-icon"
                     v-if="draggable"
        />
    </ListItem>
</template>

<script>
    import DimensionBase from "../DimensionBase";
    import ListItem from "../../List/Item";
    import LanguagePicker from "../../LanguagePicker";

    import IconEdit from "../../../../assets/icons/baseline-edit-24px.svg";
    import IconReorder from "../../../../assets/icons/baseline-reorder-24px.svg";

    /**
     * Displays a Question as a ListElement.
     *
     * Does not display all the Question's state because of space reasons. To
     * display all Question state use the Full/Question component.
     *
     * The Question will be disabled (uneditable), if it is a ShadowQuestion or
     * any Question type not owned by the current DataClient.
     */
    export default {
        name: "List-Dimension",
        extends: DimensionBase,
        components: {
            ListItem,
            LanguagePicker,
            IconEdit,
            IconReorder
        },
        props: {
            /**
             * If icons are disabled, the language picker is not available.
             */
            disableIcons: {
                type: Boolean,
                default: false
            },
            disableSubText: {
                type: Boolean,
                default: false
            },
            disableLanguagePicker: {
                type: Boolean,
                default: false
            }
        },
        computed: {
            /**
             * Returns a message displaying the number of Questions in the Di-
             * mension.
             *
             * @returns {string}
             */
            subtext() {
                return `Contains ${this.dimension.questions.length} questions.`;
            }
        },
        methods: {
            /**
             * Whether Icons on the ListElement will be needed.
             * @returns {boolean}
             */
            iconsNeeded(question) {
                return !this.disableIcons
                    && (
                        this.draggable
                        || this.convertable(question)
                        || !this.disableLanguagePicker
                    );
            },
            /**
             * Switch the Question to the given language.
             * @param {Language} language
             */
            changeLanguage(language) {
                this.dimension.fetchTranslation(language);
            },
            /**
             * Add a new translation to the Question.
             * This means set new field values via API for the given langages
             * and then fetch the question anew in the now existing language.
             * @param language
             */
            addNewTranslation(language) {
                // TODO: create new translation
                // this.question.fetchTranslation(language);
            }
        }
    }
</script>

<style lang="scss">
    .list-item.list-dimension {
        min-height: 3em;

        &.mini {
            min-height: 2em;
        }
    }
</style>
