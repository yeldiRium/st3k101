import {storiesOf} from "@storybook/vue";
import {action} from "@storybook/addon-actions";
import {boolean, text, withKnobs} from "@storybook/addon-knobs";

import ListItem from "../components/Partials/List/Item";

import IconReorder from "../assets/icons/baseline-reorder-24px.svg";
import IconExpandMore from "../assets/icons/baseline-expand_more-24px.svg";

storiesOf('ListItem', module)
    .addDecorator(withKnobs)
    .addDecorator(() => ({
        template: '<div style="display: flex; justify-content: center">' +
        '   <div style="min-width: 300px">' +
        '       <story/>' +
        '   </div>' +
        '</div>'
    }))
    .add('basic', () => ({
        components: {
            ListItem
        },
        data() {
            return {
                text: "This is a basic, editable ListElement"
            }
        },
        template: '<ListItem v-model="text" @input="action"/>',
        methods: {
            action: action("text-edited")
        }
    }))
    .add('basic with subtext', () => ({
        components: {
            ListItem
        },
        data() {
            return {
                text: "This is a basic, editable ListElement",
                subtext: "This is the element's subtext."
            }
        },
        template: '<ListItem v-model="text" :subtext="subtext" @input="action"/>',
        methods: {
            action: action("text-edited")
        }
    }))
    .add('generic', () => ({
        components: {
            ListItem,
            IconExpandMore,
            IconReorder
        },
        data() {
            return {
                text: "This is a basic, editable ListElement",
                subtext: text("Subtext", "This is the element's subtext."),
                disabled: boolean("Disabled", false),
                mini: boolean("Mini", false),
                icons: boolean("Icons", true),
                ellipseText: boolean("Ellipse Text", true),
                ellipseSubText: boolean("Ellipse Subtext", true),
                editableText: boolean("Editable Text", true)
            }
        },
        template: '<ListItem v-model="text"' +
        '                    :subtext="subtext"' +
        '                    :disabled="disabled"' +
        '                    :mini="mini"' +
        '                    :icons="icons"' +
        '                    :ellipseText="ellipseText"' +
        '                    :ellipseSubText="ellipseSubText"' +
        '                    :editableText="editableText"' +
        '                    @input="action"' +
        '          >' +
        '              <IconExpandMore class="list-item__icon"/>' +
        '              <IconReorder class="list-item__icon"/>' +
        '          </ListItem>',
        methods: {
            action: action("text-edited")
        }
    }));
