import Vue from "vue";
import Router from "vue-router";

import PublicBase from "../components/Views/Public/Base";
import SurveyForSubmission from
        "../components/Views/Public/SurveyForSubmission";

import PrivateBase from "../components/Views/Private/Base";
import Dashboard from "../components/Views/Private/Dashboard";

import TestingBase from "../components/Views/Testing/Base";
import DiamondFloatingButton from "../components/Partials/Buttons/DiamondFloatingButton";

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
            path: "/private/",
            name: "Private",
            component: PrivateBase,

            children: [
                {
                    path: "",
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
                    component: DiamondFloatingButton
                }
            ]
        }
    ]
})
