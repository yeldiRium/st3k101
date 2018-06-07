<template>
    <ListItem v-bind="$attrs"
              :text="question.text"
              :subtext="subtext"
              :disabled="disabled"
              class="question-list"
              :class="classes"
    >
        <IconEdit v-if="question.isShadow && isOwnedByCurrentDataClient"
                  class="list-item-icon"/>
        <IconReorder class="list-item-icon"/>
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
            }
        },
        computed: {
            ...mapGetters("session", ["dataClient"]),
            isOwnedByCurrentDataClient() {
                return this.question.isOwnedBy(this.dataClient);
            },
            disabled() {
                return !this.isOwnedByCurrentDataClient || this.question.isShadow;
            },
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
            }
        }
    }
</script>

<style lang="scss">

</style>