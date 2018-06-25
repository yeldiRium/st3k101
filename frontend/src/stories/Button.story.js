import {storiesOf} from "@storybook/vue";
import {action} from "@storybook/addon-actions";
import {withKnobs, text, number, boolean} from "@storybook/addon-knobs";

import Button from "../components/Partials/Form/Button";

storiesOf('Button', module)
    .addDecorator(withKnobs)
    .addDecorator(() => ({
        template: '<div style="display: flex; justify-content: center"><story/></div>'
    }))
    .add('basic', () => ({
        components: {
            Button
        },
        template: '<Button @click="action">"This is a basic Button."</Button>',
        methods: {
            action: action("button-click")
        }
    }))
    .add('noripple', () => ({
        components: {
            Button
        },
        template: '<Button @click="action" :ripple="false">"This is a Button without ripple effect."</Button>',
        methods: {
            action: action("button-click")
        }
    }))
    .add('generic', () => ({
        components: {
            Button
        },
        data() {
            return {
                text: text("Text", "This is a generic Button with many knobs."),
                elevation: number("Elevation", 0, {range: true, min: 0, max: 24, step: 1}),
                offset: number("Offset", 6, {range: true, min: 0, max: (24 - this.elevation), step: 1}),
                ripple: boolean("Ripple", true)
            }
        },
        template: '<Button @click="action" :ripple="ripple" :elevation="elevation" :offset="offset">"This is a Button without ripple effect."</Button>',
        methods: {
            action: action("button-click")
        }
    }));
