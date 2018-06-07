<template>
    <ListItem v-bind="$attrs"
              :text="question.text"
              :subtext="subtext"
              :disabled="disabled"
              class="list-question"
              :class="classes"
              :icons="iconsNeeded"
    >
        <IconEdit class="list-item-icon"
                  v-if="convertable"
        />
        <IconReorder class="list-item-icon"
                     v-if="draggable"
        />
    </ListItem>
</template>

<script>
    import {mapGetters} from "vuex";

    import {Question} from "../../../../model/Question";

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
        components: {
            ListItem,
            IconEdit,
            IconReorder
        },
        props: {
            question: {
                type: Question
            },
            draggable: {
                type: Boolean,
                default: true
            }
        },
        computed: {
            ...mapGetters("session", ["dataClient"]),
            /**
             * Whether the Question is owned by the current DataClient.
             * @returns {boolean}
             */
            isOwnedByCurrentDataClient() {
                return this.question.isOwnedBy(this.dataClient);
            },
            /**
             * Whether the Question is editable.
             * @returns {boolean}
             */
            disabled() {
                return !this.isOwnedByCurrentDataClient || this.question.isShadow;
            },
            /**
             * @returns {string}
             */
            subtext() {
                if (this.question.isShadow) {
                    return "";
                } else {
                    return `${this.question.incomingReferenceCount} references.`;
                }
            },
            classes() {
                return {
                    mini: this.question.isShadow
                };
            },
            /**
             * Whether a ShadowQuestion can be converted to a ConcreteQuestion.
             * @returns {boolean}
             */
            convertable() {
                return this.question.isShadow
                    && this.isOwnedByCurrentDataClient;
            },
            /**
             * Whether Icons on the ListElement will be needed.
             * @returns {boolean}
             */
            iconsNeeded() {
                return this.draggable || this.convertable;
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
