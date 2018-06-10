<template>
    <div class="list-question">
        test
    </div>
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
             * @returns {string}
             */
            subtext() {
                if (this.question.isShadow) {
                    return "";
                } else {
                    return `${this.question.incomingReferenceCount} references.`;
                }
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
                this.question.fetchTranslation(language);
            },
            /**
             * Add a new translation to the Question.
             * This means set new field values via API for the given lanugages
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
    .list-item.list-question {
        min-height: 3em;

        &.mini {
            min-height: 2em;
        }
    }
</style>
