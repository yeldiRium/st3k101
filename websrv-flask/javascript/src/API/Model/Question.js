import Future from "fluture";

import ResultHandling from "../Utility/ResultHandling";

export default {
    /**
     * Creates a new Question with the given text on the given hierarchy of
     * Questionnaire and QuestionGroup.
     * @param questionnaire_uuid
     * @param questionGroup_uuid
     * @param text
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "create": function (questionnaire_uuid, questionGroup_uuid, text) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch("/api/question", {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "questionnaire_uuid": questionnaire_uuid,
                    "question_group_uuid": questionGroup_uuid,
                    "text": text
                }),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    /**
     * Updates the text of the question with uuid = question_uuid to the given
     * text.
     * @param question_uuid
     * @param text
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "update": function (question_uuid, text) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/question/${question_uuid}`, {
                "method": "PUT",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "text": text
                }),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    /**
     * Deletes the Question with uuid = question_uuid on the given hierarchy of
     * Questionnaire and QuestionGroup.
     * @param question_uuid
     * @param questionnaire_uuid
     * @param questionGroup_uuid
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "delete": function (question_uuid, questionnaire_uuid, questionGroup_uuid) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/question/${question_uuid}`, {
                "method": "DELETE",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "questionnaire_uuid": questionnaire_uuid,
                    "question_group_uuid": questionGroup_uuid
                }),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    }
}
