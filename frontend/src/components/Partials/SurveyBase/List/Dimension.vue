<template>
    <ListItem class="list-dimension"
              v-bind="$attrs"
              v-on="$listeners"
              :text="dimension.name"
              :subtext="subtext"
              :mini="disableSubText"
              :disabled="!isEditable(dimension)"
              @edit="updateDimensionName"
    >
        <slot></slot>
        <LanguagePicker class="list-item-languagepicker"
                        :language-data="dimension.languageData"
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
     * Displays a Dimension as a ListElement.
     *
     * Does not display all the Dimension's state because of space reasons. To
     * display all Dimension state use the FullDimension component.
     *
     * The Dimension will be uneditable, if it is a ShadowDimension or not owned
     * by the current DataClient.
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
            disableSubText: {
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
                // TODO: clarify, when this should be available
                // TODO: create new translation
                // this.question.fetchTranslation(language);
            },
            updateDimensionName(name) {
                // TODO: set via API.
                this.dimension.name = name;
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
