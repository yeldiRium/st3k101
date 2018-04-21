import * as R from "ramda";

const getStringLanguage = R.curry(
    function (language, i15dString) {
        const defaultLanguage = R.path(
            ["fields", "default_locale"], i15dString
        );
        return R.pathOr(
            R.path(["fields", "locales", defaultLanguage], i15dString),
            ["fields", "locales", language],
            i15dString
        )
    }
);

const getDefaultStringLanguage = function (i15dString) {
    const defaultLanguage = R.path(
        ["fields", "default_locale"], i15dString
    );
    return R.path(["fields", "locales", defaultLanguage], i15dString);
};

const getSurveyTranslation = R.curry(
    function (language, survey) {
        const name = R.path(["fields", "name"], survey);
        const questionnaires = R.path(
            ["fields", "questionnaires"], survey
        );
        return R.pipe(
            R.assocPath(
                ["fields", "name"],
                getStringLanguage(language, name)
            ),
            R.assocPath(
                ["fields", "questionnaires"],
                R.map(
                    getQuestionnaireTranslation(language), questionnaires
                )
            )
        )(survey);
    }
);

const getQuestionnaireTranslation = R.curry(
    function (language, questionnaire) {
        const getString = getStringLanguage(language);

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
                    getQuestionGroupTranslation(language), questionGroups
                )
            )
        )(questionnaire);
    }
);

const getQuestionGroupTranslation = R.curry(
    function (language, questionGroup) {
        const name = R.path(["fields", "name"], questionGroup);
        const questions = R.path(
            ["fields", "questions"], questionGroup
        );
        return R.pipe(
            R.assocPath(
                ["fields", "name"],
                getStringLanguage(language, name)
            ),
            R.assocPath(
                ["fields", "questions"],
                R.map(
                    getQuestionTranslation(language), questions
                )
            )
        )(questionGroup);
    }
);

const getQuestionTranslation = R.curry(
    function (language, question) {
        const text = R.path(["fields", "text"], question);
        return R.assocPath(
            ["fields", "text"],
            getStringLanguage(language, text),
            question
        );
    }
);

const getQacTranslation = R.curry(
    function (language, qac) {
        const name = R.path(["fields", "name"], qac);
        const description = R.path(["fields", "description"], qac);
        const parameters = R.path(["fields", "parameters"], qac);
        return R.assocPath(
            ["fields", "parameters"],
            R.map(
                getQacParameterTranslation(language),
                parameters
            ),
            qac
        );
    }
);

const getQacParameterTranslation = R.curry(
    function (language, parameter) {
        if (parameter.class === "model.query_access_control.QACI15dTextParameter.QACI15dTextParameter") {
            parameter = R.assocPath(
                ["fields", "text"],
                getStringLanguage(language, R.path(["fields", "text"], parameter)),
                parameter
            );
        } else if (parameter.class === "model.query_access_control.QACCheckboxParameter.QACCheckboxParameter") {
            parameter = R.assocPath(
                ["fields", "choices"],
                R.map(
                    getDataStringContent(language),
                    R.path(["fields", "choices"])
                ),
                parameter
            );
            parameter = R.assocPath(
                ["fields", "values"],
                R.map(
                    getDataStringContent(language),
                    R.path(["fields", "values"])
                ),
                parameter
            );
        }
        return parameter;
    }
);

export default {
    "getStringLanguage": getStringLanguage,
    "getDefaultStringLanguage": getDefaultStringLanguage,
    "getSurveyTranslation": getSurveyTranslation,
    "getQuestionnaireTranslation": getQuestionnaireTranslation,
    "getQuestionGroupTranslation": getQuestionGroupTranslation,
    "getQuestionTranslation": getQuestionTranslation,
    "getQacTranslation": getQacTranslation,
    "getQacParameterTranslation": getQacParameterTranslation
}
