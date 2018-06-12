import Vue from "vue";
import Router from "vue-router";

import PublicBase from "../components/Views/Public/Base";
import SurveyForSubmission from "../components/Views/Public/SurveyForSubmission";

import PrivateBase from "../components/Views/Private/Base";
import Dashboard from "../components/Views/Private/Dashboard";
import Questionnaires from "../components/Views/Private/Questionnaires";
import Account from "../components/Views/Private/Account";

import TestingBase from "../components/Views/Testing/Base";
import TestListItem from "../components/Views/Testing/TestListItem";
import TestListQuestion from "../components/Views/Testing/TestListQuestion";
import TestFullQuestion from "../components/Views/Testing/TestFullQuestion";
import TestRangeEditor from "../components/Views/Testing/TestRangeEditor";
import TestPrivateMenuBar from "../components/Views/Testing/TestPrivateMenuBar";
import TestToggle from "../components/Views/Testing/TestToggle";
import TestModal from "../components/Views/Testing/TestModal";
import TestButton from "../components/Views/Testing/TestButton";
import TestListDimension from "../components/Views/Testing/TestListDimension";
import TestFullDimension from "../components/Views/Testing/TestFullDimension";
import TestEditableText from "../components/Views/Testing/TestEditableText";
import TestListQuestionnaire from "../components/Views/Testing/TestListQuestionnaire";
import TestFullQuestionnaire from "../components/Views/Testing/TestFullQuestionnaire";

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: "/",
            name: "PublicBase",
            component: PublicBase,

            children: [
                {
                    path: "survey/:id",
                    name: "SurveyForSubmission",
                    component: SurveyForSubmission
                }
            ]
        },
        {
            path: "/private",
            redirect: "/private/dashboard",
            name: "Private",
            component: PrivateBase,

            children: [
                {
                    path: "questionnaires",
                    name: "Questionnaires",
                    component: Questionnaires
                },
                {
                    path: "account",
                    name: "Account",
                    component: Account
                },
                {
                    path: "dashboard",
                    name: "Dashboard",
                    component: Dashboard
                }
            ]
        },
        {
            path: "/testing/",
            name: "Testing",
            component: TestingBase,

            children: [
                {
                    path: "PMB",
                    component: TestPrivateMenuBar
                },
                {
                    path: "ListItem",
                    component: TestListItem
                },
                {
                    path: "ListQuestion",
                    component: TestListQuestion
                },
                {
                    path: "FullQuestion",
                    component: TestFullQuestion
                },
                {
                    path: "RangeEditor",
                    component: TestRangeEditor
                },
                {
                    path: "Toggle",
                    component: TestToggle
                },
                {
                    path: "Modal",
                    component: TestModal
                },
                {
                    path: "Button",
                    component: TestButton
                },
                {
                    path: "ListDimension",
                    component: TestListDimension
                },
                {
                    path: "FullDimension",
                    component: TestFullDimension
                },
                {
                    path: "EditableText",
                    component: TestEditableText
                },
                {
                    path: "ListQuestionnaire",
                    component: TestListQuestionnaire
                },
                {
                    path: "FullQuestionnaire",
                    component: TestFullQuestionnaire
                }
            ]
        }
    ]
})
