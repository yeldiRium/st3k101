import Future from "fluture";
import * as R from "ramda";

import Questionnaire from "./Questionnaire";
import ResultHandling from "../Utility/ResponseHandling";
import LanguageHandling from "../Utility/LanguageHandling";
import PathHandling from "../Utility/PathHandling";

/**
 *
 * @param question_uuid
 * @returns a Future.
 * @resolves with the Question's formatted, preanalyzed statistics.
 * @rejects with either a TypeError, if a connection problem occured, or
 * with the server's response detailling the error, if the status code is
 * not 200.
 * @cancel aborts the initial HTTP request.
 */
let get = function (question_uuid) {
    return Future((reject, resolve) => {
        const controller = new AbortController();
        const signal = controller.signal;

        fetch(PathHandling.buildApiPath(`/api/question/${question_uuid}/statistic`), {
            "method": "GET",
            "mode": "cors",
            "credentials": "include",
            signal
        })
            .then(resolve)
            .catch(reject);

        return controller.abort;
    })
        .chain(ResultHandling.checkStatus(200))
        .chain(ResultHandling.extractJson)
        .chainRej(ResultHandling.extractJson)
        .map(result => ({
            "biggest": R.path(["fields", "biggest"], result),
            "smallest": R.path(["fields", "smallest"], result),
            "q1": R.path(["fields", "q1"], result),
            "q2": R.path(["fields", "q2"], result),
            "q3": R.path(["fields", "q3"], result),
            "answer_count": R.path(
                ["fields", "answer_count"],
                result
            )
        }));
};

/**
 * Formats the given question and statisticsResult according to the language.
 *
 * @param question
 * @param language
 * @param statisticResult
 */
let formatQuestionResult = R.curry(
    function (language, question, statisticResult) {
        return {
            "text": LanguageHandling.getStringLanguage(
                language, question.fields.text
            ),
            "answers": statisticResult.answer_count,
            "statistic": statisticResult
        }
    }
);

export default {
    "get": get,
    /**
     *
     * @param questionnaire_uuid
     * @returns a Future
     * @resolves with a formatted statistics object for a whole Questionnaire.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP requests.
     */
    "getWholeQuestionnaire": function (questionnaire_uuid) {
        return Questionnaire
            .get(questionnaire_uuid)
            .map(({data: questionnaireData, language}) => {
                return R.pipe(
                    R.map(questionGroup => ({
                        "name": questionGroup.fields.name,
                        "color": questionGroup.fields.color,
                        "text_color": questionGroup.fields.text_color,
                        "questions": questionGroup.fields.questions
                    })),
                    R.map(questionGroup => R.assoc(
                        "questions",
                        R.map(
                            question => get(question.uuid)
                                .map(formatQuestionResult(language, question)),
                            questionGroup.questions
                        ),
                        questionGroup
                    )),
                    R.map(questionGroup =>
                        Future.parallel(
                            Infinity,
                            questionGroup.questions
                        )
                            .map(questions => {
                                return R.assoc(
                                    "questions",
                                    questions,
                                    questionGroup
                                )
                            })
                    ))
                (questionnaireData.fields.questiongroups);
            })
            .chain(questionGroups => {
                return Future.parallel(
                    Infinity,
                    questionGroups
                );
            });
    },
    /**
     * Updates the preanalyzed statistics on the server side.
     *
     * @param questionnaire_uuid
     * @param force
     * @returns a Future
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP requests.
     */
    "update": function (questionnaire_uuid, force = false) {
        let path;
        if (force) {
            path = "/api/statistics/update/force";
        } else {
            path = "/api/statistics/update";
        }
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(PathHandling.buildApiPath(path), {
                "method": "POST",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    }
}
