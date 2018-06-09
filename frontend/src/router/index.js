import Vue from "vue";
import Router from "vue-router";

import PublicBase from "../components/Views/Public/Base";
import SurveyForSubmission from "../components/Views/Public/SurveyForSubmission";

import PrivateBase from "../components/Views/Private/Base";
import Dashboard from "../components/Views/Private/Dashboard";
import Questionnaires from "../components/Views/Private/Questionnaires";
import Account from "../components/Views/Private/Account";

import TestingBase from "../components/Views/Testing/Base";
import TestDiamondFloatingButton from "../components/Views/Testing/TestDiamondFloatingButton";
import TestButtonBar from "../components/Views/Testing/TestButtonBar";
import TestListItem from "../components/Views/Testing/TestListItem";
import TestListQuestion from "../components/Views/Testing/TestListQuestion";
import TestFullQuestion from "../components/Views/Testing/TestFullQuestion";
import TestRangeEditor from "../components/Views/Testing/TestRangeEditor";

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
                    path: "DFB",
                    name: "DiamondFloatingButton",
                    component: TestDiamondFloatingButton
                },
                {
                    path: "ButtonBar",
                    name: "ButtonBar",
                    component: TestButtonBar
                },
                {
                    path: "ListItem",
                    name: "ListItem",
                    component: TestListItem
                },
                {
                    path: "ListQuestion",
                    name: "ListQuestion",
                    component: TestListQuestion
                },
                {
                    path: "FullQuestion",
                    name: "FullQuestion",
                    component: TestFullQuestion
                },
                {
                    path: "RangeEditor",
                    name: "RangeEditor",
                    component: TestRangeEditor
                }
            ]
        }
    ]
})
