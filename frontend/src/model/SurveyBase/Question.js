import Future from "fluture";

import SurveyBase from "./SurveyBase";

import Range from "./Config/Range";
import {fetchQuestion} from "../../api/Question";

/**
 * BaseClass for ShadowQuestion and ConcreteQuestion.
 * Don't instantiate this. Only use the extensions. If JavaScript had abstract
 * classes, this would be one.
 */
class Question extends SurveyBase {
    /**
     * @param {string}  href See Resource.
     * @param {String} id See Resource.
     * @param {Party}   owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string}  text The Question text.
     * @param {Range}   range The range for the Question's answer.
     */
    constructor(href,
                id,
                owner,
                languageData,
                text, range) {
        super(href, id, owner, languageData);

        this.text = text;
        this.range = range;
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

    // TODO: implement fetchTranslation(language)
}

/**
 * A ConcreteQuestion is a Question which can be referenced from
 * ShadowQuestions. It is a real Question with own, editable content.
 */
class ConcreteQuestion extends Question {
    /**
     * @param {String}  href See Resource.
     * @param {String} id See Resource.
     * @param {Party}   owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string}  text See Question.
     * @param {Range}   range See Question.
     * @param {number}  incomingReferenceCount Number of references to this
     *  Question.
     *  This counts references not owned by the current user and can thus be
     *  bigger than the number of ownedIncomingReferences.
     * @param {Array.<Resource|ShadowQuestion>} ownedIncomingReferences List of
     *  all references (in form of hrefs or ShadowQuestion instances) to this
     *  Question, which the current user owns.
     */
    constructor(href,
                id,
                owner,
                languageData,
                text,
                range,
                incomingReferenceCount, ownedIncomingReferences) {
        if (incomingReferenceCount < ownedIncomingReferences.length) {
            throw new Error("ReferenceCount can't be smaller than list of owned references.");
        }

        super(href, id, owner, languageData, text, range);
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
     * @param {String} id See Resource.
     * @param {Party}   owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string}  text See Question.
     * @param {Range}   range See Question.
     * @param {Resource|ConcreteQuestion} referenceTo Href or instance of the
     *  referenced Question.
     */
    constructor(href,
                id,
                owner,
                languageData,
                text,
                range, referenceTo) {
        super(href, id, owner, languageData, text, range);
        this.referenceTo = referenceTo;
    }

    get isShadow() {
        return true;
    }

    get isConcrete() {
        return false;
    }
}

/**
 * Takes in a Question and populates its incoming references field by replacing
 * all resolvable References with their corresponding ShadowQuestion instances.
 *
 * Accesses the API to load the Questions.
 *
 * If this rejects, then some questions might be populated and some might still
 * be Resources. The exact state will have to be tested.
 *
 * @param {ConcreteQuestion} concreteQuestion
 * @return {Future}
 * @resolve with nothing, since the change is made in place.
 * @reject with an API error message.
 * @cancel
 */
function populateOwnedIncomingReferences(concreteQuestion) {
    const resolvedShadowQuestionFutures = [];

    // Use basic for loop to easily replace values.
    for (let i = 0; i < concreteQuestion.ownedIncomingReferences.length; i++) {
        /** @type {Resource|ShadowQuestion} */
        let reference = concreteQuestion.ownedIncomingReferences[i];

        if (instanceOf(reference, Resource)) {
            const shadowQuestionFuture = fetchQuestion({href: reference.href})
                .chain(shadowQuestion => {
                    concreteQuestion.ownedIncomingReferences[i] =
                        shadowQuestion;
                    return Future.of(shadowQuestion);
                });

            resolvedShadowQuestionFutures.push(shadowQuestionFuture);
        }
    }
    // MAYBE: is Infinity appropriate?
    return Future.parallel(Infinity, resolvedShadowQuestionFutures);
}

/**
 * If the referenceTo field contains a Resource, it is resolved to a
 * ConcreteQuestion instance. Otherwise it is left as is.
 *
 * Accesses the API to load the Question.
 *
 * If this rejects, the referenceTo property was not replaced. It might still be
 * a Resource.
 *
 * TODO: implement this. currently it replaces the reference with an empty
 *       object.
 *
 * @param {ShadowQuestion} shadowQuestion
 * @return {Future}
 * @resolve with nothing, since the change is made in place.
 * @reject with an API error message.
 * @cancel
 */
function populateReferenceTo(shadowQuestion) {
    if (instanceOf(shadowQuestion.referenceTo, Resource)) {
        const shadowQuestionFuture = fetchQuestion({
            href: shadowQuestion.referenceTo.href
        })
            .chain(shadowQuestion => {
                shadowQuestion.referenceTo = concreteQuestion;
                return Future.of(shadowQuestion);
            });
    }
}

/**
 * Based on the type of the given Question this either populates its incoming
 * references or its referenceTo field.
 *
 * @param {Question} question
 * @return {Future}
 * @resolve with nothing, since the change is made in place.
 * @reject with an API error message.
 * @cancel
 */
function populateQuestion(question) {
    // Type warnings can be ignored, since they are tested.
    if (instanceOf(question, ShadowQuestion)) {
        return populateReferenceTo(question);
    }
    if (instanceOf(question, ConcreteQuestion)) {
        return populateOwnedIncomingReferences(question);
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
