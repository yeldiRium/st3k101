import Vue from "vue";
import Router from "vue-router";

import PublicBase from "../components/Views/Public/Base";
import SurveyForSubmission from "../components/Views/Public/SurveyForSubmission";
import Authentication from "../components/Views/Public/Authentication";

import PrivateBase from "../components/Views/Private/Base";
import Dashboard from "../components/Views/Private/Dashboard";
import MyQuestionnaires from "../components/Views/Private/MyQuestionnaires";
import Account from "../components/Views/Private/Account";
import AQuestion from "../components/Views/Private/AQuestion";
import ADimension from "../components/Views/Private/ADimension";
import AQuestionnaire from "../components/Views/Private/AQuestionnaire";

import TestingBase from "../components/Views/Testing/Base";
import TestListItem from "../components/Views/Testing/TestListItem";
import TestQuestion from "../components/Views/Testing/TestQuestion";
import TestRangeEditor from "../components/Views/Testing/TestRangeEditor";
import TestPrivateMenuBar from "../components/Views/Testing/TestPrivateMenuBar";
import TestToggle from "../components/Views/Testing/TestToggle";
import TestModal from "../components/Views/Testing/TestModal";
import TestButton from "../components/Views/Testing/TestButton";
import TestDimension from "../components/Views/Testing/TestDimension";
import TestEditableText from "../components/Views/Testing/TestEditableText";
import TestQuestionnaire from "../components/Views/Testing/TestQuestionnaire";
import TestLoadingSpinnerModal from "../components/Views/Testing/TestLoadingSpinnerModal";

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
                },
                {
                    path: "authentication",
                    name: "Authentication",
                    component: Authentication
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
                    path: "dashboard",
                    name: "Dashboard",
                    component: Dashboard
                },
                {
                    path: "questionnaires",
                    name: "MyQuestionnaires",
                    component: MyQuestionnaires
                },
                {
                    path: "account",
                    name: "Account",
                    component: Account
                },
                {
                    path: "question/:id",
                    name: "AQuestion",
                    component: AQuestion
                },
                {
                    path: "dimension/:id",
                    name: "ADimension",
                    component: ADimension
                },
                {
                    path: "questionnaire/:id",
                    name: "AQuestionnaire",
                    component: AQuestionnaire
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
                    path: "Question",
                    component: TestQuestion
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
                    path: "Dimension",
                    component: TestDimension
                },
                {
                    path: "EditableText",
                    component: TestEditableText
                },
                {
                    path: "Questionnaire",
                    component: TestQuestionnaire
                },
                {
                    path: "LoadingSpinnerModal",
                    component: TestLoadingSpinnerModal
                }
            ]
        }
    ]
})
