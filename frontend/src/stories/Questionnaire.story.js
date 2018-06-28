import {mapGetters} from "vuex-fluture";
import {storiesOf} from "@storybook/vue";
import {boolean, withKnobs} from "@storybook/addon-knobs";
import {action} from "@storybook/addon-actions";
import StoryRouter from "storybook-vue-router";

import Questionnaire from "../components/Partials/SurveyBase/Questionnaire";
import Dialog from "../components/Partials/Modal/Dialog";
import CreateQuestion from "../components/Partials/Modal/CreateQuestion";
import CreateDimension from "../components/Partials/Modal/CreateDimension";
import TranslateQuestion from "../components/Partials/Modal/TranslateQuestion";
import TranslateDimension from "../components/Partials/Modal/TranslateDimension";
import TranslateQuestionnaire from "../components/Partials/Modal/TranslateQuestionnaire";

import store from "./Fixtures/TestStore";

storiesOf('Questionnaire', module)
    .addDecorator(StoryRouter())
    .addDecorator(withKnobs)
    .addDecorator(() => ({
        components: {
            Dialog,
            CreateQuestion,
            CreateDimension,
            TranslateQuestion,
            TranslateDimension,
            TranslateQuestionnaire
        },
        template: '<div style="display: grid; justify-items: center; grid-row-gap: 50px">' +
        '   <div v-for="n in 10" :style="{\'width\': `${100 * n + 50}px`}">' +
        '       {{ 100 * n + 50 }}px: <story/>' +
        '   </div>' +
        '   <Dialog />' +
        '   <CreateQuestion />' +
        '   <CreateDimension />' +
        '   <TranslateQuestion />' +
        '   <TranslateDimension />' +
        '   <TranslateQuestionnaire />' +
        '</div>',
        store
    }))
    .add('basic', () => ({
        components: {
            Questionnaire
        },
        data() {
            return {
                showLink: boolean("Show Link", true)
            }
        },
        computed: {
            ...mapGetters("questionnaires", ["questionnaire"])
        },
        template: '<Questionnaire :questionnaire="questionnaire" :show-link="showLink" @questionnaire-delete="questionnaireDelete"/>',
        store,
        methods: {
            questionnaireDelete: action("questionnaire-delete")
        }
    }));
