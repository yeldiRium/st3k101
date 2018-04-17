import Future from "fluture";

import ResultHandling from "../Utility/ResultHandling";

export default {
    /**
     * Creates a new QuestionGroup with the given name on the given Question-
     * naire.
     * @param questionnaire_uuid
     * @param name
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "create": function (questionnaire_uuid, name) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch("/api/question_group", {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "questionnaire_uuid": questionnaire_uuid,
                    "name": name,
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
     * Updates the given QuestionGroup's data.
     * @param questionGroup_uuid
     * @param name
     * @param color
     * @param textColor
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "update": function (questionGroup_uuid,
                        {name = null, color = null, textColor = null}) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/question_group/${questionGroup_uuid}`, {
                "method": "PUT",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "name": name,
                    "color": color,
                    "text_color": textColor
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
     * Deletes the given QuestionGroup from the Questionnaire.
     * @param questionGroup_uuid
     * @param questionnaire_uuid
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "delete":
        function (questionGroup_uuid, questionnaire_uuid) {
            return Future((reject, resolve) => {
                const controller = new AbortController();
                const signal = controller.signal;

                fetch(`/api/question_group/${questionGroup_uuid}`, {
                    "method": "DELETE",
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "mode": "cors",
                    "credentials": "include",
                    "body": JSON.stringify({
                        "questionnaire_uuid": questionnaire_uuid
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
