import {isRangeValid} from "./Range";

/**
 * BaseClass for ShadowQuestion and ConcreteQuestion.
 * Don't instantiate this. Only use the extensions. If JavaScript had abstract
 * classes, this would be one.
 */
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
     */
    constructor(text,
                {start = 0, end, step = 1},
                isOwn) {
        if (!isRangeValid({start, end, step})) {
            throw new Error(`Invalid range options: {start: ${start}, end: ${end}, step: ${step}.`);
        }

        this._text = text;
        this._range = {start, end, step};
        this._isOwn = isOwn;
    }

    /**
     * Getter for text.
     * Setter only in ConcreteQuestion.
     * @returns {string}
     */
    get text() {
        return this._text;
    }

    /**
     * Getter for range.
     * Setter only in ConcreteQuestion.
     * @returns {{start: number, end: number, step: number}}
     */
    get range() {
        return this._range;
    }

    /**
     * Getter for isOwn.
     * This is read-only.
     * @returns {boolean}
     */
    get isOwn() {
        return this._isOwn;
    }

    /**
     * True, if this Question is a ShadowQuestion.
     *
     * @returns {boolean}
     */
    isShadow() {
        throw new Error("Please override this.");
    };

    /**
     * True, if this Question is a ConcreteQuestion.
     *
     * @returns {boolean}
     */
    isConcrete() {
        throw new Error("Please override this.");
    }
}

/**
 * A ConcreteQuestion is a Question which can be referenced from
 * ShadowQuestions. It is a real Question with own, editable content.
 */
class ConcreteQuestion extends Question {
    /**
     * @param {string}  text See Question.
     * @param {number}  start See Question.
     * @param {number}  end See Question.
     * @param {number}  step See Question.
     * @param {boolean} isOwn See Question.
     * @param {number}  referenceCount Number of references to this Question.
     *  This counts references not owned by the current user and can thus be
     *  bigger than the number of ownedReferences.
     * @param {Array.<string>} ownedReferences List of all references (in form of
     *  hrefs) to this Question, which the current user owns.
     */
    constructor(text,
                {start = 0, end, step = 1},
                isOwn,
                referenceCount,
                ownedReferences) {
        super(text, {start, end, step}, isOwn);
        this.referenceCount = referenceCount;
        this.ownedReferences = ownedReferences;
    }

    /**
     * Setter for text.
     * @param {string} text
     */
    set text(text) {
        this._text = text;
    }

    /**
     * Setter for range.
     * @param {number} start
     * @param {number} end
     * @param {number} step
     */
    set range({start = 0, end, step = 1}) {
        this._range = {start, end, step};
    }

    isShadow() {
        return false;
    }

    isConcrete() {
        return true;
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
 * A ShadowQuestion is a reference to a ConcreteQuestion and is immutable, since
 * its content is just a shadow of the reference.
 */
class ShadowQuestion extends Question {
    /**
     * @param {string}  text See Question.
     * @param {number}  start See Question.
     * @param {number}  end See Question.
     * @param {number}  step See Question.
     * @param {boolean} isOwn See Question.
     * @param {string} referenceTo Href of the referenced Question.
     *  If this is set, this Question is a ShadowQuestion.
     *  If this is not set (null), this Question is a ConcreteQuestion.
     */
    constructor(text,
                {start = 0, end, step = 1},
                isOwn,
                referenceTo = null) {
        super(text, {start, end, step}, isOwn);
        this.referenceTo = referenceTo;
    }

    isShadow() {
        return true;
    }

    isConcrete() {
        return false;
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
    ConcreteQuestion,
    ShadowQuestion,
    getOwnedReferencesToQuestion
}