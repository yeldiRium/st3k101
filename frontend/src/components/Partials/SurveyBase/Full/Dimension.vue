<template>
    <div class="full-dimension"
         :class="classes"
         v-if="expanded"
    >
        <ListDimension :dimension="dimension"
                       :disableSubText="true"
                       :draggable="true"
                       :ellipseText="false"
                       @click="toggleExpanded"
                       :disableEditing="disableEditing"
        />

        <div class="full-dimension-body"
             ref="dropdown"
             v-if="expanded"
        >
            <ReferenceCounter :object="dimension"
                              v-if="dimension.isConcrete"
            />

            <Toggle v-model="dimension.randomizeQuestions">
                <template slot="off">
                    in order
                </template>
                <template slot="on">
                    randomize
                </template>
            </Toggle>

            <div class="full-dimension-questions">
                <FullQuestion v-for="question in dimension.questions"
                              :key="question.href"
                              :question="question"
                              :disableEditing="disableEditingQuestion(question)"
                />

                <ListItem class="full-dimension-add-question"
                          v-if="editable(dimension)"
                          text="Add new Question"
                          :disableSubtext="true"
                          @click="addNewQuestion"
                />
                <CreateQuestion v-if="editable(dimension)"
                                :language="dimension.languageData.currentLanguage"
                                @question-created="handleCreatedQuestion"
                />
            </div>

            <div class="full-dimension-delete"
                 v-if="!disabled(dimension)"
            >
                delete
            </div>
        </div>
    </div>
    <div class="full-dimension"
         :class="classes"
         v-else
    >
        <ListDimension :dimension="dimension"
                       :draggable="draggable"
                       :ellipseText="true"
                       @click="toggleExpanded"
                       :disableEditing="disableEditing"
        />
    </div>
</template>

<script>
    import {mapState} from "vuex";

    import DimensionBase from "../DimensionBase";
    import ListDimension from "../List/Dimension";
    import FullQuestion from "../Full/Question";
    import ListItem from "../../List/Item";
    import CreateQuestion from "../../Popup/CreateQuestion";

    import ReferenceCounter from "../Config/ReferenceCounter";
    import Toggle from "../../Form/Toggle";

    export default {
        name: "Full-Dimension",
        extends: DimensionBase,
        components: {
            ListDimension,
            FullQuestion,
            CreateQuestion,
            ListItem,
            ReferenceCounter,
            Toggle
        },
        props: {
            initiallyExpanded: {
                type: Boolean,
                default: false
            }
        },
        data() {
            return {
                expanded: false,
                header: {
                    height: 0
                },
                dropdown: {
                    height: 0
                }
            }
        },
        computed: {
            classes() {
                return {
                    disabled: this.disabled(this.dimension)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            disableEditingQuestion(question) {
                return !this.isOwnedByCurrentDataClient(this.dimension)
                    || this.dimension.isShadow;
            },
            addNewQuestion() {
                this.$modal.show(
                    "create-question",
                    {}
                )
            },
            handleCreatedQuestion(question) {
                // TODO: update dimension via API.
                this.dimension.questions.push(question);
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .list-item.list-dimension {
        cursor: pointer;

        background-color: $primary;

        &.disabled {
            background-color: $slightlylight;
        }
    }

    .full-dimension {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &.disabled {
            background-color: $lighter;
        }

        &-questions {
            width: 95%;

            display: flex;
            flex-flow: column;
        }

        .full-dimension-add-question {
            background-color: $primary;
        }

        .toggle {
            > div {
                color: $darker;
            }

            &-off.toggle-off-active,
            &-on.toggle-on-active {
                color: $verydark;
            }
        }
    }

    .full-dimension-body {
        display: flex;
        flex-flow: column;
        align-items: center;

        > * {
            margin-top: 8px;
            margin-bottom: 8px;
        }
    }
</style>
