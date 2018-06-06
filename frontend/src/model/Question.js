import {isRangeValid} from "./Range";

class Question {
    /**
     * Constructs the full Question with valid data.
     *
     * @param {string}  text The Question text.
     * @param {number}  start Start of the range interval. Defaults to 0.
     * @param {number}  end End of the range interval.
     * @param {number}  step Step of the range interval. Defaults to 1.
     * @param {boolean} isOwn Whether this Question is owned by the current
     *  user.
     * @param {number}  referenceCount Number of references to this Question.
     *  This counts references not owned by the current user and can thus be
     *  bigger than the number of ownedReferences.
     *  If isShadow is true, this must be 0.
     * @param {Array.<string>} ownedReferences List of all references (in form of
     *  hrefs) to this Question, which the current user owns.
     *  If isShadow is true, this must be an empty Array.
     * @param {string} referenceTo Href of the referenced Question.
     *  If this is set, this Question is a ShadowQuestion.
     *  If this is not set (null), this Question is a ConcreteQuestion.
     */
    constructor(text,
                {start = 0, end, step = 1},
                isOwn,
                referenceCount,
                ownedReferences,
                referenceTo = null) {
        if (!isRangeValid({start, end, step})) {
            throw new Error(`Invalid range options: {start: ${start}, end: ${end}, step: ${step}.`);
        }

        if (
            referenceTo !== null
            && (referenceCount > 0 || ownedReferences.length > 0)
        ) {
            throw new Error("A ShadowQuestion can't be referenced!");
        }

        if (referenceCount < 0) {
            throw new Error("ReferenceCount can't be less than zero!");
        }

        this.text = text;
        this.range = {start, end, step};
        this.isOwn = isOwn;
        this.referenceTo = referenceTo;
        this.referenceCount = referenceCount;
        this.ownedReferences = ownedReferences;
    }

    /**
     * True, if this Question is a ShadowQuestion.
     *
     * @returns {boolean}
     */
    isShadow() {
        return this.referenceTo !== null;
    }

    /**
     * Number of reference to this Question, which are owned by the current
     * user.
     *
     * @returns {number}
     */
    ownedReferenceCount() {
        return this.ownedReferences.length;
    }
}

/**
 * Takes in a Question and returns an Array of all references to that Question.
 *
 * Accesses the API to load the Questions.
 * Should this provide context to the Questions? Or should that be done via
 * mapping another function over this function's result?
 *
 * @param {Question} question
 * @return {Array.<Question>}
 */
function getOwnedReferencesToQuestion(question) {
    // TODO: implement
}

export default Question;

export {
    Question,
    getOwnedReferencesToQuestion
}