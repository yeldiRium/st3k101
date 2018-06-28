import Vuex from "vuex-fluture";
import {isNil} from "ramda";
import {action} from "@storybook/addon-actions";

import {
    initialize as initializeGlobalStore,
    store as global
} from "../../store/modules/Global";

import Language, {LanguageData} from "../../model/Language";
import Resource from "../../model/Resource";
import DataClient from "../../model/DataClient";
import Range from "../../model/SurveyBase/Config/Range";
import {
    ConcreteQuestion,
    ShadowQuestion
} from "../../model/SurveyBase/Question";
import {
    ConcreteDimension,
    ShadowDimension
} from "../../model/SurveyBase/Dimension";
import {ConcreteQuestionnaire} from "../../model/SurveyBase/Questionnaire";

const english = new Language("en", "English");
const german = new Language("de", "Deutsch");
const spanish = new Language("es", "Espanol");
const italian = new Language("it", "Italiano");

const languageData = new LanguageData(
    english,
    english,
    [english, german]
);

const dataClient = new DataClient(
    "http://localhost:1337/api/dataclient/1",
    1,
    "data.client@data.client",
    english
);

const question1 = new ConcreteQuestion("http://localhost:1337/api/question/2", 2, [dataClient], languageData, false, "Question Text", new Range({
    start: 0,
    end: 10
}), 3, []);

const question2 = new ShadowQuestion(
    "http://localhost:1337/api/question/3",
    3,
    [dataClient],
    languageData,
    "Question Text",
    new Range({start: 0, end: 10}),
    question1
);
question1.ownedIncomingReferences.push(question2);

const dimension1 = new ConcreteDimension("http://localhost:1337/api/dimension/4", 4, [dataClient], languageData, "Dimension name", [question1, question2], false, 5, [], false);

const dimension2 = new ShadowDimension(
    "http://localhost:1337/api/dimension/5",
    5,
    [dataClient],
    languageData,
    "Dimension name",
    [question1, question2],
    false,
    dimension1
);
dimension1.ownedIncomingReferences.push(dimension2);

const questionnaire1 = new ConcreteQuestionnaire("http://localhost:1337/api/questionnaire/6", 6, [dataClient], languageData, false, "Questionnaire name", "Questionnaire description", true, true, "xapi target", [dimension1, dimension2], 2, []);

const store = new Vuex.Store({
    modules: {
        global,
        language: {
            namespaced: true,
            state: {
                languages: [
                    english,
                    german,
                    spanish,
                    italian
                ]
            },
            actions: {
                fetchLanguages: action("languages-fetched")
            },
        },
        session: {
            namespaced: true,
            state: {
                dataClient: dataClient
            },
            getters: {
                dataClient: state => state.dataClient
            }
        },
        questions: {
            namespaced: true,
            state: {
                question: question1
            },
            getters: {
                question: state => state.question
            },
            actions: {
                fetchQuestion: action("question-fetched"),
                updateQuestion({commit}, {params}) {
                    commit("updateQuestion", {params});
                    action("question-updated")(params);
                    return question1;
                }
            },
            mutations: {
                updateQuestion(state, {params}) {
                    for (const key in params) {
                        if (!isNil(state.question[key])) {
                            state.question[key] = params[key];
                        }
                    }
                }
            }
        },
        dimensions: {
            namespaced: true,
            state: {
                dimension: dimension1
            },
            getters: {
                dimension: state => state.dimension
            },
            actions: {
                fetchDimension: action("dimension-fetched"),
                updateDimension({commit}, {params}) {
                    commit("updateDimension", {params});
                    action("dimension-updated")(params);
                    return dimension1;
                },
                addConcreteQuestion: action("concreteQuestion-added"),
                removeQuestion: action("question-removed")
            },
            mutations: {
                updateDimension(state, {params}) {
                    for (const key in params) {
                        if (!isNil(state.dimension[key])) {
                            state.dimension[key] = params[key];
                        }
                    }
                }
            }
        },
        questionnaires: {
            namespaced: true,
            state: {
                questionnaire: questionnaire1
            },
            getters: {
                questionnaire: state => state.questionnaire
            },
            actions: {
                fetchQuestionnaire: action("questionnaire-fetched"),
                updateQuestionnaire({commit}, {params}) {
                    commit("updateQuestionnaire", {params});
                    action("questionnaire-updated")(params);
                    return questionnaire1;
                },
                addConcreteDimension: action("concreteDimension-added"),
                removeDimension: action("dimension-removed")
            },
            mutations: {
                updateQuestionnaire(state, {params}) {
                    for (const key in params) {
                        if (!isNil(state.questionnaire[key])) {
                            state.questionnaire[key] = params[key];
                        }
                    }
                }
            }
        }
    }
});

initializeGlobalStore(store, "global")
    .fork(
        console.error,
        () => {
        }
    );

export default store;
