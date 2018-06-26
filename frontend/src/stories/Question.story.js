import {mapGetters} from "vuex-fluture";
import {storiesOf} from "@storybook/vue";
import {boolean, withKnobs} from "@storybook/addon-knobs";
import StoryRouter from "storybook-vue-router";

import Question from "../components/Partials/SurveyBase/Question";

import store from "./Fixtures/TestStore";

storiesOf('Question', module)
    .addDecorator(StoryRouter())
    .addDecorator(withKnobs)
    .addDecorator(() => ({
        template: '<div style="display: grid; justify-items: center; grid-row-gap: 50px">' +
        '   <div v-for="n in 10" :style="{\'min-width\': `${100 * n + 50}px`}">' +
        '       {{ 100 * n + 50 }}px: <story/>' +
        '   </div>' +
        '</div>'
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
        template: '<Question :question="question" :show-link="showLink"/>',
        store: store
    }));
