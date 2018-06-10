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
                }
            ]
        }
    ]
})
