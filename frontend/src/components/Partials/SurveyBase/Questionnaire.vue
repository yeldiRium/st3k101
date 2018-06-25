<template>
    <div class="questionnaire"
         :class="classes"
    >
        <ListItem class="questionnaire__title"
                  :value="questionnaire.name"
                  :subtext="subtext"
                  :mini="expanded"
                  :ellipseText="!expanded"
                  :disabled="!isEditable(questionnaire)"
                  @input="updateQuestionnaireName"
        >
            <router-link :to="{name: 'AQuestionnaire', params: {id: questionnaire.id}}">
                <IconLink class="list-item__icon"
                          v-if="showLink"
                />
            </router-link>
            <template>
                <IconExpandLess class="list-item__icon"
                                v-if="expanded"
                                @click.native="toggleExpanded"
                />
                <IconExpandMore class="list-item__icon"
                                v-else
                                @click.native="toggleExpanded"
                />
            </template>
            <LanguagePicker class="list-item__language-picker"
                            :language-data="questionnaire.languageData"
                            @choose-language="changeLanguage"
                            @choose-language-unavailable="addNewTranslation"
            />
            <IconReorder class="list-item__icon"
                         v-if="draggable"
            />
        </ListItem>

        <div class="questionnaire__body"
             v-if="expanded"
             ref="dropdown"
        >
            <ReferenceCounter :object="questionnaire"
                              v-if="questionnaire.isConcrete"
            />

            <template>
                <EditableText v-if="questionnaire.isConcrete"
                              :value="questionnaire.description"
                              @input="updateDescription"
                              :textArea="true"
                />
                <div v-else>
                    {{ questionnaire.description }}
                </div>
            </template>

            <Toggle :value="questionnaire.isPublic"
                    :disabled="!isOwnedByCurrentDataClient(questionnaire)"
                    @input="updateIsPublic"
            >
                <template slot="off">
                    locked
                </template>
                <template slot="on">
                    published
                </template>
            </Toggle>

            <Toggle :value="questionnaire.allowEmbedded"
                    :disabled="!isOwnedByCurrentDataClient(questionnaire)"
                    @input="updateAllowEmbedded"
            >
                <template slot="off">
                    only in browser
                </template>
                <template slot="on">
                    allow embedding
                </template>
            </Toggle>

            <EditableText :value="questionnaire.xapiTarget"
                          @input="updateXapiTarget"
            />

            <div class="questionnaire__dimensions">
                <Dimension class="dimension--bordered"
                           v-for="dimension in questionnaire.dimensions"
                           :key="dimension.href"
                           :dimension="dimension"
                           :deletable="questionnaire.isConcrete"
                           @dimension-delete="deleteDimension"
                />
            </div>
        </div>
        <div class="questionnaire__buttons"
             v-if="expanded"
        >
            <Button v-if="isEditable(questionnaire)"
                    @click="openNewDimensionDialog"
            >
                Add new Dimension
            </Button>
            <Button v-if="isDeletable(questionnaire)"
                    @click="deleteQuestionnaire"
            >
                delete
            </Button>
        </div>
    </div>
</template>

<script>
    import {mapState} from "vuex-fluture";
    import {map, path, sum, without} from "ramda";

    import {Questionnaire} from "../../../model/SurveyBase/Questionnaire";

    import SurveyBase from "./SurveyBase";
    import Dimension from "./Dimension";
    import ListItem from "../List/Item";
    import EditableText from "../Form/EditableText";
    import LanguagePicker from "../LanguagePicker";
    import ReferenceCounter from "./Config/ReferenceCounter";
    import Toggle from "../Form/ToggleButton";
    import Button from "../Form/Button";

    import IconLink from "../../../assets/icons/baseline-link-24px.svg";
    import IconExpandLess from "../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../assets/icons/baseline-expand_more-24px.svg";
    import IconReorder from "../../../assets/icons/baseline-reorder-24px.svg";

    export default {
        name: "Questionnaire",
        extends: SurveyBase,
        components: {
            ListItem,
            Dimension,
            LanguagePicker,
            ReferenceCounter,
            Toggle,
            EditableText,
            Button,
            IconLink,
            IconReorder,
            IconExpandLess,
            IconExpandMore
        },
        props: {
            /** @type {Questionnaire} */
            questionnaire: {
                type: Questionnaire
            },
            initiallyExpanded: {
                type: Boolean,
                default: false
            },
            showLink: {
                type: Boolean,
                default: true
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
            ...mapState("session", ["dataClient"]),
            classes() {
                return {
                    "questionnaire--disabled": !this.isEditable(this.questionnaire)
                }
            },
            /**
             * Returns a message displaying the number of Dimensions and Ques-
             * tions in the Questionnaire.
             *
             * @returns {string}
             */
            subtext() {
                let questionCount = sum(
                    map(
                        path(["questions", "length"]),
                        this.questionnaire.dimensions
                    )
                );
                return `Contains ${this.questionnaire.dimensions.length} dimensions and ${questionCount} questions.`;
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            /**
             * Switch the Questionnaire to the given language.
             * @param {Language} language
             */
            changeLanguage(language) {
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/fetchQuestionnaire",
                        {href: this.questionnaire.href, language}
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            /**
             * Add a new translation to the Questionnaire.
             * This means set new field values via API for the given languages
             * and then fetch the questionnaire anew in the now existing language.
             * @param language
             */
            addNewTranslation(language) {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                // TODO: display dialog which asks for data
                const name = "tbd";
                const description = "tbd";

                this.$load(
                    this.$store.dispatch(
                        "questionnaires/updateQuestionnaire",
                        {
                            questionnaire: this.questionnaire,
                            language,
                            params: {
                                name,
                                description
                            }
                        }
                    )
                        .chain(
                            questionnaire => this.$store.dispatch(
                                "questionnaires/fetchQuestionnaire",
                                {href: questionnaire.href, language}
                            )
                        )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            updateQuestionnaireName(name) {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/updateQuestionnaire",
                        {
                            questionnaire: this.questionnaire,
                            params: {name}
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            updateDescription(description) {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/updateQuestionnaire",
                        {
                            questionnaire: this.questionnaire,
                            params: {description}
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            updateIsPublic(isPublic) {
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/updateQuestionnaire",
                        {
                            questionnaire: this.questionnaire,
                            params: {isPublic}
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            updateAllowEmbedded(allowEmbedded) {
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/updateQuestionnaire",
                        {
                            questionnaire: this.questionnaire,
                            params: {allowEmbedded}
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            updateXapiTarget(xapiTarget) {
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/updateQuestionnaire",
                        {
                            questionnaire: this.questionnaire,
                            params: {xapiTarget}
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            openNewDimensionDialog() {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$modal.show(
                    "modal-create-dimension",
                    {
                        language: this.questionnaire.languageData.currentLanguage,
                        handler: this.createDimension
                    }
                )
            },
            createDimension({name, randomizeQuestions}) {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/addConcreteDimension",
                        {
                            questionnaire: this.questionnaire,
                            params: {
                                name,
                                randomizeQuestions
                            }
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            deleteDimension(dimension) {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/removeDimension",
                        {
                            questionnaire: this.questionnaire,
                            dimension
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            /**
             * Asks for confirmation, if the Questionnaire should be deleted, and
             * emits an event commanding to do so, if the user confirms.
             */
            deleteQuestionnaire() {
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
                                handler: () => this.$emit(
                                    "questionnaire-delete",
                                    this.questionnaire
                                ),
                                default: true
                            }
                        ]
                    }
                )
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .questionnaire {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &--disabled {
            background-color: $lighter;
        }

        &--bordered {
            border: 1px solid $primary;

            &.questionnaire--disabled {
                border-color: $slightlylight;
            }
        }

        &__add-dimension-button {
            background-color: $primary;
        }

        &__body {
            display: flex;
            flex-flow: column;
            align-items: center;

            > * {
                width: 95%;
                margin-top: 8px;
                margin-bottom: 8px;
            }

            > *:not(.questionnaire__dimensions) {
                text-align: center;
            }
        }

        &__dimensions {
            display: flex;
            flex-flow: column;
        }

        &__buttons {
            display: flex;
            justify-content: center;

            margin-bottom: 8px;

            .button {
                margin: 0 8px 0 8px;
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
