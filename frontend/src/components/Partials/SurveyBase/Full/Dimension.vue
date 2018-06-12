<template>
    <div class="full-dimension"
         :class="classes"
         v-if="expanded"
    >
        <ListDimension :dimension="dimension"
                       :disableSubText="true"
                       :draggable="true"
                       :ellipseText="false"
        >
            <IconExpandLess class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListDimension>

        <div class="full-dimension__body"
             ref="dropdown"
        >
            <ReferenceCounter :object="dimension"
                              v-if="dimension.isConcrete"
            />

            <Toggle v-model="dimension.randomizeQuestions"
                    :disabled="!isOwnedByCurrentDataClient(dimension)"
            >
                <template slot="off">
                    in order
                </template>
                <template slot="on">
                    randomize
                </template>
            </Toggle>

            <div class="full-dimension__questions">
                <FullQuestion v-for="question in dimension.questions"
                              :key="question.href"
                              :question="question"
                              :deletable="dimension.isConcrete"
                              @question-deleted="handleDeletedQuestion"
                />

                <ListItem class="full-dimension__add-question-button"
                          v-if="isEditable(dimension)"
                          text="Add new Question"
                          :disableSubtext="true"
                          @click="addNewQuestion"
                />
                <CreateQuestion v-if="isEditable(dimension)"
                                :language="dimension.languageData.currentLanguage"
                                @question-created="handleCreatedQuestion"
                />
            </div>

            <div class="full-dimension__delete-button"
                 v-if="isDeletable(dimension)"
                 @click="confirmDeleteDimension"
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
        >
            <IconExpandMore class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListDimension>
    </div>
</template>

<script>
    import {without} from "ramda";

    import DimensionBase from "../DimensionBase";
    import ListDimension from "../List/Dimension";
    import FullQuestion from "../Full/Question";
    import ListItem from "../../List/Item";
    import CreateQuestion from "../../Modal/CreateQuestion";

    import ReferenceCounter from "../Config/ReferenceCounter";
    import Toggle from "../../Form/ToggleButton";

    import IconExpandLess from "../../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../../assets/icons/baseline-expand_more-24px.svg";

    export default {
        name: "FullDimension",
        extends: DimensionBase,
        components: {
            ListDimension,
            FullQuestion,
            CreateQuestion,
            ListItem,
            ReferenceCounter,
            Toggle,
            IconExpandLess,
            IconExpandMore
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
                    "full-dimension--disabled": !this.isEditable(this.dimension)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            addNewQuestion() {
                this.$modal.show(
                    "modal-create-question"
                )
            },
            handleCreatedQuestion(question) {
                // TODO: update dimension via API.
                this.dimension.questions.push(question);
            },
            handleDeletedQuestion(question) {
                // TODO: delete via api
                this.dimension.questions = without(
                    [question],
                    this.dimension.questions
                );
            },
            /**
             * Asks for confirmation, if the Dimension should be deleted, and
             * does so if the user confirms.
             */
            confirmDeleteDimension() {
                this.$modal.show(
                    "dialog",
                    {
                        title: `Really delete Dimension?`,
                        text: `Do you really want to delete Dimension "${this.dimension.name}"?`,
                        buttons: [
                            {
                                text: "Cancel"
                            },
                            {
                                text: "Confirm",
                                handler: () => this.deleteDimension(),
                                default: true
                            }
                        ]
                    }
                )
            },
            deleteDimension() {
                // TODO: delete via api
                this.$emit("dimension-deleted", this.dimension);
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .full-dimension {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &--disabled {
            background-color: $lighter;
        }

        &__questions {
            width: 95%;

            display: flex;
            flex-flow: column;
        }

        &__add-question-button {
            background-color: $primary;
        }

        &__body {
            display: flex;
            flex-flow: column;
            align-items: center;

            > * {
                margin-top: 8px;
                margin-bottom: 8px;
            }
        }

        .toggle-button {
            > div {
                color: $darker;
            }

            &--off-side.toggle-button__off-side--active,
            &--on-side.toggle-button__on-side--active {
                color: $verydark;
            }
        }

        .list-dimension.list-item {
            background-color: $primary;

            &--disabled {
                background-color: $slightlylight;
            }
        }
    }
</style>
