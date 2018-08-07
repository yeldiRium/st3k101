class SubmissionQuestion {
    constructor(id,
                href,
                text,
                range,
                languageData
    ) {
        this.id = id;
        this.href = href;
        this.text = text;
        this.range = range;
        this.languageData = languageData;
        this.value = -1;
    }

    clone() {
        return new SubmissionQuestion(
            this.id,
            this.href,
            this.text,
            this.range,
            this.languageData
        );
    }

    /**
     * @param {SubmissionQuestion} otherSubmissionQuestion
     * @returns {boolean} true, if both have the same id
     */
    equals(otherSubmissionQuestion) {
        return this.id === otherSubmissionQuestion.id;
    }
}

export default SubmissionQuestion;

export {
    SubmissionQuestion
};
