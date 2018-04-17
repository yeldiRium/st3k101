import * as R from "ramda";

const getStringLocale = R.curry(
    function (locale, i15dString) {
        const defaultLocale = R.path(
            ["fields", "default_locale"], i15dString
        );
        return R.pathOr(
            R.path(["fields", "locales", defaultLocale], i15dString),
            ["fields", "locales", locale],
            i15dString
        )
    }
);

const getDefaultStringLocale = function (i15dString) {
    const defaultLocale = R.path(
        ["fields", "default_locale"], i15dString
    );
    return R.path(["fields", "locales", defaultLocale], i15dString);
};

const getSurveyTranslation = R.curry(
    function (locale, survey) {
        const name = R.path(["fields", "name"], survey);
        const questionnaires = R.path(
            ["fields", "questionnaires"], survey
        );
        return R.pipe(
            R.assocPath(
                ["fields", "name"],
                getStringLocale(locale, name)
            ),
            R.assocPath(
                ["fields", "questionnaires"],
                R.map(
                    getQuestionnaireTranslation(locale), questionnaires
                )
            )
        )(survey);
    }
);

const getQuestionnaireTranslation = R.curry(
    function (locale, questionnaire) {
        const getString = getStringLocale(locale);

        const name = R.path(["fields", "name"], questionnaire);
        const description = R.path(
            ["fields", "description"], questionnaire
        );
        const questionGroups = R.path(
            ["fields", "questiongroups"], questionnaire
        );
        return R.pipe(
            R.assocPath(
                ["fields", "name"],
                getString(name)
            ),
            R.assocPath(
                ["fields", "description"],
                getString(description)
            ),
            R.assocPath(
                ["fields", "questiongroups"],
                R.map(
                    getQuestionGroupTranslation(locale), questionGroups
                )
            )
        )(questionnaire);
    }
);

const getQuestionGroupTranslation = R.curry(
    function (locale, questionGroup) {
        const name = R.path(["fields", "name"], questionGroup);
        const questions = R.path(
            ["fields", "questions"], questionGroup
        );
        return R.pipe(
            R.assocPath(
                ["fields", "name"],
                getStringLocale(locale, name)
            ),
            R.assocPath(
                ["fields", "questions"],
                R.map(
                    getQuestionTranslation(locale), questions
                )
            )
        )(questionGroup);
    }
);

const getQuestionTranslation = R.curry(
    function (locale, question) {
        const text = R.path(["fields", "text"], question);
        return R.assocPath(
            ["fields", "text"],
            getStringLocale(locale, text),
            question
        );
    }
);

const getQacTranslation = R.curry(
    function (locale, qac) {
        const name = R.path(["fields", "name"], qac);
        const description = R.path(["fields", "description"], qac);
        const parameters = R.path(["fields", "parameters"], qac);
        return R.assocPath(
            ["fields", "parameters"],
            R.map(
                getQacParameterTranslation(locale),
                parameters
            ),
            qac
        );
    }
);

const getQacParameterTranslation = R.curry(
    function (locale, parameter) {
        if (parameter.class === "model.query_access_control.QACI15dTextParameter.QACI15dTextParameter") {
            parameter = R.assocPath(
                ["fields", "text"],
                getStringLocale(locale, R.path(["fields", "text"], parameter)),
                parameter
            );
        } else if (parameter.class === "model.query_access_control.QACCheckboxParameter.QACCheckboxParameter") {
            parameter = R.assocPath(
                ["fields", "choices"],
                R.map(
                    getDataStringContent(locale),
                    R.path(["fields", "choices"])
                ),
                parameter
            );
            parameter = R.assocPath(
                ["fields", "values"],
                R.map(
                    getDataStringContent(locale),
                    R.path(["fields", "values"])
                ),
                parameter
            );
        }
        return parameter;
    }
);

export default {
    "getStringLocale": getStringLocale,
    "getDefaultStringLocale": getDefaultStringLocale,
    "getSurveyTranslation": getSurveyTranslation,
    "getQuestionnaireTranslation": getQuestionnaireTranslation,
    "getQuestionGroupTranslation": getQuestionGroupTranslation,
    "getQuestionTranslation": getQuestionTranslation,
    "getQacTranslation": getQacTranslation,
    "getQacParameterTranslation": getQacParameterTranslation
}
