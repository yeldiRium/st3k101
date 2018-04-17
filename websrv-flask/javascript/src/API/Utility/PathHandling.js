export default {
    "openQuestionnaire": function (questionnaire_uuid) {
        const win = window.open(
            `/survey/${questionnaire_uuid}`, "_blank"
        );
        if (win) {
            win.focus();
            return true;
        }
        return false;
    }
}
