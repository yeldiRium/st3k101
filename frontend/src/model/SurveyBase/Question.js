import Future from "fluture";

import SurveyBase from "./SurveyBase";

import Range from "./Config/Range";

/**
 * BaseClass for ShadowQuestion and ConcreteQuestion.
 * Don't instantiate this. Only use the extensions. If JavaScript had abstract
 * classes, this would be one.
 */
class Question extends SurveyBase {
    /**
     * @param {string}  href See Resource.
     * @param {Party}   owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string}  text The Question text.
     * @param {Range}   range The range for the Question's answer.
     */
    constructor(href,
                owner,
                languageData,
                text,
                range) {
        super(href, owner, languageData);

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
                owner,
                languageData,
                text,
                range,
                incomingReferenceCount,
                ownedIncomingReferences) {
        if (incomingReferenceCount < ownedIncomingReferences.length) {
            throw new Error("ReferenceCount can't be smaller than list of owned references.");
        }

        super(href, owner, languageData, text, range);
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
     * @param {Party}   owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string}  text See Question.
     * @param {Range}   range See Question.
     * @param {Resource|ConcreteQuestion} referenceTo Href or instance of the
     *  referenced Question.
     */
    constructor(href,
                owner,
                languageData,
                text,
                range,
                referenceTo) {
        super(href, owner, languageData, text, range);
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
 * TODO: implement. currently this replaces all Resource-type references with
 *       empty objects.
 *
 * @param {ConcreteQuestion} concreteQuestion
 * @return {Future}
 * @resolve with nothing, since the change is made in place.
 * @reject with an API error message.
 * @cancel TODO: can this actually be cancelled?
 */
function populateOwnedIncomingReferences(concreteQuestion) {
    const resolvedShadowQuestionFutures = [];

    // Use basic for loop to easily replace values.
    for (let i = 0; i < concreteQuestion.ownedIncomingReferences.length; i++) {
        let reference = concreteQuestion.ownedIncomingReferences[i];

        if (instanceOf(reference, Resource)) {
            // TODO: fetch ShadowQuestion and replace
            const shadowQuestionFuture = Future.of({}) // <- replace with actual API call
                .map(shadowQuestion => {
                    concreteQuestion.ownedIncomingReferences[i] =
                        shadowQuestion;
                    return true;
                });

            resolvedShadowQuestionFutures.push(shadowQuestionFuture);
        }
    }
    return Future.parallel(Infinity, resolvedShadowQuestionFutures);
}

/**
 * If the referenceTo field contains a Resource, it is resolved to a
 * ConcreteQuestion instance. Otherwise it is left as is.
 *
 * Accesses the API to load the Question.
 *
 * If it is invalid or does not resolve to anything, an error is thrown.
 *
 * TODO: implement this. currently it replaces the reference with an empty
 *       object.
 *
 * @param {ShadowQuestion} shadowQuestion
 * @return {Future}
 * @resolve with nothing, since the change is made in place.
 * @reject with an API error message.
 * @cancel TODO: can this actually be cancelled?
 */
function populateReferenceTo(shadowQuestion) {
    if (instanceOf(shadowQuestion.referenceTo, Resource)) {
        // TODO: fetch ConcreteQuestion and replace
        return Future.of({}) // <- replace with actual API call
            .map(concreteQuestion => {
                shadowQuestion.referenceTo = concreteQuestion;
            });
    }
    return Future.of(true);
}

/**
 * Based on the type of the given Question this either populates its incoming
 * references or its referenceTo field.
 *
 * @param {Question} question
 * @return {Future}
 * @resolve with nothing, since the change is made in place.
 * @reject with an API error message.
 * @cancel TODO: can this actually be cancelled?
 */
function populateQuestion(question) {
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