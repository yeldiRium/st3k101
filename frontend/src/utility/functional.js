import * as R from "ramda";

/**
 * allTrue :: [Boolean] -> Boolean
 *
 * Predicate that is true if a given list contains only true Booleans.
 *
 * @param {Array<Boolean>} xs
 */
function allTrue(xs) {
  return R.reduce(R.and, true, xs);
}

/**
 * anyTrue :: [Boolean] -> Boolean
 *
 * Predicate that is true if a given list contains one or more true Booleans.
 *
 * @param {Array<Boolean>} xs
 */
function anyTrue(xs) {
  return R.reduce(R.or, false, xs);
}

/**
 * allContentsEqual :: a -> a -> Boolean
 *
 * Predicate that is true if contents of a and b match.
 * a and b need to implement the contentEquals method.
 *
 * @param a
 * @param b
 * @returns {Boolean}
 */
function allContentsEqual(a, b) {
  return allTrue(R.zipWith((a, b) => a.contentEquals(b), a, b));
}

export { allTrue, anyTrue, allContentsEqual };
