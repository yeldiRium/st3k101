import {assoc, curry, dissoc, has, pipe, prop, when} from "ramda";

/**
 * Removes oldProp from obj and adds newProp to obj with the value from oldProp.
 *
 * If oldProp is not found on obj, no newProp is added.
 *
 * @param {String} oldProp Name of the prop to remove.
 * @param {String} newProp Namo of the prop to add.
 * @param {Object} obj The object in question.
 *
 * @return {Object}
 */
const renameProp = curry((oldProp, newProp, obj) => {
    return when(
        has(oldProp),
        pipe(
            obj => assoc(newProp, prop(oldProp, obj), obj),
            dissoc(oldProp)
        )
    )(obj);
});

export default renameProp;
