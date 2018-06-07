<template>
    <ListItem class="list-question"
              v-bind="$attrs"
              :text="question.text"
              :subtext="subtext"
              :mini="question.isShadow || disableSubText"
              :disabled="disabled(question)"
              :icons="iconsNeeded(question)"
    >
        <IconEdit class="list-item-icon"
                  v-if="convertable(question)"
        />
        <IconReorder class="list-item-icon"
                     v-if="draggable"
        />
    </ListItem>
</template>

<script>
    import QuestionBase from "../QuestionBase";
    import ListItem from "../../List/Item";

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
        name: "List-Question",
        extends: QuestionBase,
        components: {
            ListItem,
            IconEdit,
            IconReorder
        },
        props: {
            disableIcons: {
                type: Boolean,
                default: false
            },
            disableSubText: {
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
                    && (this.draggable || this.convertable(question));
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
