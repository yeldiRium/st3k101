import {storiesOf} from '@storybook/vue';

import Button from "../components/Partials/Form/Button";

storiesOf('Button', module)
    .addDecorator(() => ({
        template: '<div style="display: flex; justify-content: center"><story/></div>'
    }))
    .add('basic button', () => ({
        components: {
            Button
        },
        template: '<Button @click="handler1">This is a Button</Button>',
        methods: {
            handler1() {
                alert("Button 1 clicked!");
            },
        }
    }));
