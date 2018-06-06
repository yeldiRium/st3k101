<template>
    <ListItem v-bind="$attrs"
              :text="question.text"
              :subtext="subtext"
              :disabled="disabled"
              class="question"
              :class="classes"
    >
        <IconEdit v-if="question.isShadow && isOwnedByCurrentDataClient"
                  class="list-item-icon"/>
        <IconReorder class="list-item-icon"/>
    </ListItem>
</template>i

<script>
    import {mapGetters} from "vuex";

    import {Question} from "../../../model/Question";

    import ListItem from "./Item";

    import IconEdit from "../../../assets/icons/baseline-edit-24px.svg";
    import IconReorder from "../../../assets/icons/baseline-reorder-24px.svg";

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