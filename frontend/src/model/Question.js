import OwnedResource from "./OwnedResource";

import {isRangeValid} from "./Range";

/**
 * BaseClass for ShadowQuestion and ConcreteQuestion.
 * Don't instantiate this. Only use the extensions. If JavaScript had abstract
 * classes, this would be one.
 */
class Question extends OwnedResource {
    /**
     * @param {string}  href See Resource.
     * @param {Party}   owner See OwnedResource.
     * @param {string}  text The Question text.
     * @param {number}  start Start of the range interval. Defaults to 0.
     * @param {number}  end End of the range interval.
     * @param {number}  step Step of the range interval. Defaults to 1.
     */
    constructor(href,
                owner,
                text,
                {start = 0, end, step = 1}) {
        super(href, owner);

        if (!isRangeValid({start, end, step})) {
            throw new Error(`Invalid range options: {start: ${start}, end: ${end}, step: ${step}.`);
        }

        this._text = text;
        this._range = {start, end, step};
    }

    /**
     * True, if this Question is a ShadowQuestion.
     *
     * @returns {boolean}
     */
    get isShadow() {
        throw new Error("Please override this.");
    };

    /**
     * True, if this Question is a ConcreteQuestion.
     *
     * @returns {boolean}
     */
    get isConcrete() {
        throw new Error("Please override this.");
    }

    /**
     * Getter for text.
     * Setter only in ConcreteQuestion.
     * @returns {string}
     */
    get text() {
        throw new Error("Please override this.");
    }

    /**
     * Getter for range.
     * Setter only in ConcreteQuestion.
     * @returns {{start: number, end: number, step: number}}
     */
    get range() {
        throw new Error("Please override this.");
    }
}

/**
 * A ConcreteQuestion is a Question which can be referenced from
 * ShadowQuestions. It is a real Question with own, editable content.
 */
class ConcreteQuestion extends Question {
    /**
     * @param {String}  href See Resource.
     * @param {Party}   owner See OwnedResource.
     * @param {string}  text See Question.
     * @param {number}  start See Question.
     * @param {number}  end See Question.
     * @param {number}  step See Question.
     * @param {number}  incomingReferenceCount Number of references to this
     *  Question.
     *  This counts references not owned by the current user and can thus be
     *  bigger than the number of ownedIncomingReferences.
     * @param {Array.<Resource|ShadowQuestion>} ownedIncomingReferences List of
     *  all references (in form of hrefs or ShadowQuestion instances) to this
     *  Question, which the current user owns.
     */
    constructor(href,
                owner,
                text,
                {start = 0, end, step = 1},
                incomingReferenceCount,
                ownedIncomingReferences) {
        if (incomingReferenceCount < ownedIncomingReferences.length) {
            throw new Error("ReferenceCount can't be smaller than list of owned references.");
        }

        super(href, owner, text, {start, end, step});
        this.incomingReferenceCount = incomingReferenceCount;
        this.ownedIncomingReferences = ownedIncomingReferences;
    }

    get isShadow() {
        return false;
    }

    get isConcrete() {
        return true;
    }

    /**
     * Setter for text.
     * @param {string} text
     */
    set text(text) {
        this._text = text;
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
     * Setter for range.
     * @param {number} start
     * @param {number} end
     * @param {number} step
     */
    set range({start = 0, end, step = 1}) {
        this._range = {start, end, step};
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
     * Number of reference to this Question, which are owned by the current
     * user.
     *
     * @returns {number}
     */
    ownedIncomingReferenceCount() {
        return this.ownedIncomingReferences.length;
    }
}

/**
 * A ShadowQuestion is a reference to a ConcreteQuestion and is immutable, since
 * its content is just a shadow of the reference.
 */
class ShadowQuestion extends Question {
    /**
     * @param {String}  href See Resource.
     * @param {Party}   owner See OwnedResource.
     * @param {string}  text See Question.
     * @param {number}  start See Question.
     * @param {number}  end See Question.
     * @param {number}  step See Question.
     * @param {Resource|ConcreteQuestion} referenceTo Href or instance of the
     *  referenced Question.
     */
    constructor(href,
                owner,
                text,
                {start = 0, end, step = 1},
                referenceTo) {
        super(href, owner, text, {start, end, step});
        this.referenceTo = referenceTo;
    }

    get isShadow() {
        return true;
    }

    get isConcrete() {
        return false;
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
}

/**
 * Takes in a Question and populates its incoming references field.
 * Removes all elements in the references array which are neither Resources nor
 * ShadowQuestions and fetches a ShadowQuestion for each Resource (if possible).
 * If a reference of type Resource can't be resolved to a ShadowQuestion, it is
 * removed.
 *
 * Accesses the API to load the Questions.
 *
 * TODO: implement. currently this just removes all references of type Resource
 *       and everything that is neither Resource nor ShadowQuestion.
 *
 * @param {ConcreteQuestion} concreteQuestion
 */
function populateOwnedIncomingReferences(concreteQuestion) {
    const resolvedShadowQuestions = [];
    for (const reference in concreteQuestion.ownedIncomingReferences) {
        if (instanceOf(reference, ShadowQuestion)) {
            resolvedShadowQuestions.push(reference);
            continue;
        }
        if (instanceOf(reference, Resource)) {
            // TODO: fetch ShadowQuestion and replace
            // const newShadowQuestion = ...
            // resolvedShadowQuestions.push(newShadowQuestion);
        }
    }
    concreteQuestion.ownedIncomingReferences = resolvedShadowQuestions;
    return concreteQuestion;
}

/**
 * If the referenceTo field contains a Resource, it is resolved to a
 * ConcreteQuestion instance. Otherwise it is left as is.
 *
 * If it is invalid or does not resolve to anything, an error is thrown.
 *
 * TODO: implement this. currently it does nothing
 *
 * @param {ShadowQuestion} shadowQuestion
 */
function populateReferenceTo(shadowQuestion) {
    if (instanceOf(shadowQuestion.referenceTo, ConcreteQuestion)) {
        return;
    }
    if (instanceOf(shadowQuestion.referenceTo, Resource)) {
        // TODO: fetch ConcreteQuestion and replace
        return;
    }
    throw new Error("ReferenceTo value was invalid!");
}

/**
 * Based on the type of the given Question this either populates its incoming
 * references or its referenceTo field.
 *
 * @param {Question} question
 */
function populateQuestion(question) {
    if (instanceOf(question, ShadowQuestion)) {
        populateReferenceTo(question);
    }
    if (instanceOf(question, ConcreteQuestion)) {
        populateOwnedIncomingReferences(question);
    }
}

export default Question;

export {
    Question,
    ConcreteQuestion,
    ShadowQuestion,
    populateOwnedIncomingReferences,
    populateReferenceTo,
    populateQuestion
}