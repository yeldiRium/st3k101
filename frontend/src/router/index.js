import Vue from "vue";
import Router from "vue-router";

import PublicBase from "../components/Views/Public/Base";
import SurveyForSubmission from "../components/Views/Public/SurveyForSubmission";
import EmbeddedSurveyForSubmission from "../components/Views/Embedded/EmbeddedSurveyForSubmission"
import Authentication from "../components/Views/Public/Authentication";

import PrivateBase from "../components/Views/Private/Base";
import Dashboard from "../components/Views/Private/Dashboard";
import MyQuestionnaires from "../components/Views/Private/MyQuestionnaires";
import Account from "../components/Views/Private/Account";
import AQuestion from "../components/Views/Private/AQuestion";
import ADimension from "../components/Views/Private/ADimension";
import AQuestionnaire from "../components/Views/Private/AQuestionnaire";

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
            path: "/embedded",
            name: "Embedded",
            component: EmbeddedSurveyForSubmission
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
                    path: "questionnaires/question/:id",
                    name: "AQuestion",
                    component: AQuestion
                },
                {
                    path: "questionnaires/dimension/:id",
                    name: "ADimension",
                    component: ADimension
                },
                {
                    path: "questionnaires/questionnaire/:id",
                    name: "AQuestionnaire",
                    component: AQuestionnaire
                }
            ]
        }
    ]
})
