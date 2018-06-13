<template>
    <div class="full-questionnaire"
         :class="classes"
         v-if="expanded"
    >
        <ListQuestionnaire :questionnaire="questionnaire"
                           :disableSubText="true"
                           :draggable="true"
                           :ellipseText="false"
        >
            <IconExpandLess class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListQuestionnaire>

        <div class="full-questionnaire__body"
             ref="dropdown"
        >
            <ReferenceCounter :object="questionnaire"
                              v-if="questionnaire.isConcrete"
            />

            <Toggle v-model="questionnaire.randomizeDimensions"
                    :disabled="!isOwnedByCurrentDataClient(questionnaire)"
            >
                <template slot="off">
                    in order
                </template>
                <template slot="on">
                    randomize
                </template>
            </Toggle>

            <div class="full-questionnaire__dimensions">
                <FullDimension class="full-dimension--bordered"
                               v-for="dimension in questionnaire.dimensions"
                               :key="dimension.href"
                               :dimension="dimension"
                               :deletable="questionnaire.isConcrete"
                               @dimension-deleted="handleDeletedDimension"
                />

                <ListItem class="full-questionnaire__add-dimension-button"
                          v-if="isEditable(questionnaire)"
                          text="Add new Dimension"
                          :disableSubtext="true"
                          :editableText="false"
                          @click="addNewDimension"
                />
                <CreateDimension v-if="isEditable(questionnaire)"
                                 :language="questionnaire.languageData.currentLanguage"
                                 @dimension-created="handleCreatedDimension"
                />
            </div>

            <div class="full-questionnaire__delete-button"
                 v-if="isDeletable(questionnaire)"
                 @click="confirmDeleteQuestionnaire"
            >
                delete
            </div>
        </div>
    </div>
    <div class="full-questionnaire"
         :class="classes"
         v-else
    >
        <ListQuestionnaire :questionnaire="questionnaire"
                           :draggable="draggable"
                           :ellipseText="true"
        >
            <IconExpandMore class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListQuestionnaire>
    </div>
</template>

<script>
    import {without} from "ramda";

    import QuestionnaireBase from "../QuestionnaireBase";
    import ListQuestionnaire from "../List/Questionnaire";
    import FullDimension from "../Full/Dimension";
    import ListItem from "../../List/Item";

    import CreateDimension from "../../Modal/CreateDimension";

    import ReferenceCounter from "../Config/ReferenceCounter";
    import Toggle from "../../Form/ToggleButton";

    import IconExpandLess from "../../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../../assets/icons/baseline-expand_more-24px.svg";

    export default {
        name: "Full-Questionnaire",
        extends: QuestionnaireBase,
        components: {
            ListQuestionnaire,
            FullDimension,
            CreateDimension,
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
                    "full-questionnaire--disabled": !this.isEditable(this.questionnaire)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            addNewDimension() {
                this.$modal.show(
                    "modal-create-dimension"
                )
            },
            handleCreatedDimension(dimension) {
                // TODO: update questionnaire via API.
                this.questionnaire.dimensions.push(dimension);
            },
            handleDeletedDimension(dimension) {
                // TODO: delete via api
                this.questionnaire.dimensions = without(
                    [dimension],
                    this.questionnaire.dimensions
                );
            },
            /**
             * Asks for confirmation, if the Questionnaire should be deleted, and
             * does so if the user confirms.
             */
            confirmDeleteQuestionnaire() {
                this.$modal.show(
                    "dialog",
                    {
                        title: `Really delete Questionnaire?`,
                        text: `Do you really want to delete Questionnaire "${this.questionnaire.name}"?`,
                        buttons: [
                            {
                                text: "Cancel"
                            },
                            {
                                text: "Confirm",
                                handler: () => this.deleteQuestionnaire(),
                                default: true
                            }
                        ]
                    }
                )
            },
            deleteQuestionnaire() {
                // TODO: delete via api
                this.$emit("questionnaire-deleted", this.questionnaire);
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .full-questionnaire {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &--disabled {
            background-color: $lighter;
        }

        &--bordered {
            border: 1px solid $primary;

            &.full-questionnaire--disabled {
                border-color: $slightlylight;
            }
        }

        &__dimensions {
            width: 95%;

            display: flex;
            flex-flow: column;
        }

        &__add-dimension-button {
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

</style>
