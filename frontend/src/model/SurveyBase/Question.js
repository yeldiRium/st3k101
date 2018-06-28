import SurveyBase from "./SurveyBase";

import Range from "./Config/Range";
import {clone, map} from "ramda";

/**
 * BaseClass for ShadowQuestion and ConcreteQuestion.
 * Don't instantiate this. Only use the extensions. If JavaScript had abstract
 * classes, this would be one.
 */
class Question extends SurveyBase {
    /**
     * @param {string}  href See Resource.
     * @param {String} id See Resource.
     * @param {Array<Party>} owners See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {Boolean} template See SurveyBase.
     * @param {string}  text The Question text.
     * @param {Range}   range The range for the Question's answer.
     */
    constructor(href,
                id,
                owners,
                languageData,
                template,
                text,
                range) {
        super(href, id, owners, languageData, template);

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

    /**
     * @returns {Question}
     */
    clone() {
        return new Question(
            this._href,
            this._id,
            [...this._owners],
            this.languageData.clone(),
            this.template,
            this.text,
            this.range.clone()
        );
    }
}

/**
 * A ConcreteQuestion is a Question which can be referenced from
 * ShadowQuestions. It is a real Question with own, editable content.
 */
class ConcreteQuestion extends Question {
    /**
     * @param {String}  href See Resource.
     * @param {String} id See Resource.
     * @param {Array<Party>} owners See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {Boolean} template See SurveyBase.
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
                owners,
                languageData,
                template,
                text,
                range,
                incomingReferenceCount,
                ownedIncomingReferences) {
        if (incomingReferenceCount < ownedIncomingReferences.length) {
            throw new Error("ReferenceCount can't be smaller than list of owned references.");
        }

        super(href, id, owners, languageData, template, text, range);
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

    /**
     * @returns {ConcreteQuestion}
     */
    clone() {
        return new ConcreteQuestion(
            this._href,
            this._id,
            [...this._owners],
            this.languageData.clone(),
            this.template,
            this.text,
            this.range.clone(),
            this.incomingReferenceCount,
            map(clone, this.ownedIncomingReferences)
        );
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
     * @param {Array<Party>} owners See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string}  text See Question.
     * @param {Range}   range See Question.
     * @param {Resource|ConcreteQuestion} referenceTo Href or instance of the
     *  referenced Question.
     */
    constructor(href,
                id,
                owners,
                languageData,
                text,
                range,
                referenceTo) {
        super(href, id, owners, languageData, false, text, range);
        this.referenceTo = referenceTo;
    }

    get isShadow() {
        return true;
    }

    get isConcrete() {
        return false;
    }

    /**
     * @returns {ShadowQuestion}
     */
    clone() {
        return new ShadowQuestion(
            this._href,
            this._id,
            [...this._owners],
            this.languageData.clone(),
            this.text,
            this.range.clone(),
            this.referenceTo.clone()
        );
    }
}

export default Question;

export {
    Question,
    ConcreteQuestion,
    ShadowQuestion
}
