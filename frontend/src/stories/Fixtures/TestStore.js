import Vuex from "vuex-fluture";
import {action} from "@storybook/addon-actions";
import Language, {LanguageData} from "../../model/Language";
import DataClient from "../../model/DataClient";
import {ConcreteQuestion} from "../../model/SurveyBase/Question";
import Range from "../../model/SurveyBase/Config/Range";
import Resource from "../../model/Resource";

import {
    initialize as initializeGlobalStore,
    store as global
} from "../../store/modules/Global";

const english = new Language("en", "English");
const german = new Language("de", "Deutsch");
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
const concreteQuestion = new ConcreteQuestion(
    "http://localhost:1337/api/question/2",
    2,
    [dataClient],
    languageData,
    "Question Text",
    new Range({start: 0, end: 10}),
    3,
    [
        new Resource("http://localhost:1337/api/question/3", 3)
    ]
);

const store = new Vuex.Store({
    modules: {
        global,
        language: {
            namespaced: true,
            state: {
                currentLanguage: {
                    short: "de",
                    long: "Deutsch"
                },
                languageOptions: [],
                languages: [
                    new Language("de", "German"),
                    new Language("en", "English"),
                    new Language("it", "Italian"),
                    new Language("es", "Spanish"),
                    new Language("ch", "Chinese")
                ]
            },
            actions: {
                fetchLanguages: action("languages-fetched")
            },
        },
        session: {
            namespaced: true,
            getters: {
                dataClient: () => dataClient
            }
        },
        questions: {
            namespaced: true,
            getters: {
                question: () => concreteQuestion
            },
            actions: {
                fetchQuestion: action("question-fetched"),
                updateQuestion() {
                    action("question-updated")();
                    return concreteQuestion;
                }
            }
        }
    }
});

initializeGlobalStore(store, "global")
    .fork(
        console.error,
        console.log
    );

export default store;
