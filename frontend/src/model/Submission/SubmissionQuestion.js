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
}

export default SubmissionQuestion;

export {
    SubmissionQuestion
};