import {mapGetters} from "vuex-fluture";
import {storiesOf} from "@storybook/vue";
import {boolean, withKnobs} from "@storybook/addon-knobs";
import {action} from "@storybook/addon-actions";
import StoryRouter from "storybook-vue-router";

import Question from "../components/Partials/SurveyBase/Question";
import Dialog from "../components/Partials/Modal/Dialog";
import TranslateQuestion from "../components/Partials/Modal/TranslateQuestion";

import store from "./Fixtures/TestStore";

storiesOf('Question', module)
    .addDecorator(StoryRouter())
    .addDecorator(withKnobs)
    .addDecorator(() => ({
        components: {
            Dialog,
            TranslateQuestion
        },
        template: '<div style="display: grid; justify-items: center; grid-row-gap: 50px">' +
        '   <div v-for="n in 10" :style="{\'min-width\': `${100 * n + 50}px`}">' +
        '       {{ 100 * n + 50 }}px: <story/>' +
        '   </div>' +
        '   <Dialog />' +
        '   <TranslateQuestion />' +
        '</div>',
        store
    }))
    .add('basic', () => ({
        components: {
            Question
        },
        data() {
            return {
                showLink: boolean("Show Link", true)
            }
        },
        computed: {
            ...mapGetters("questions", ["question"])
        },
        template: '<Question :question="question" :show-link="showLink" @question-delete="questionDelete"/>',
        store,
        methods: {
            questionDelete: action("question-delete")
        }
    }));
