/**
 * Immutable Range object.
 */
class Range {
    /**
     * @param {number} start
     * @param {number} end
     * @param {number} step
     */
    constructor({start = 0, end, step = 1}) {
        if (start > end) {
            throw new Error("Range start can't be bigger than end.");
        }
        if (step <= 0) {
            throw new Error("Step must be bigger than 0.");
        }
        if (
            (Math.round(start) !== start)
            || (Math.round(end) !== end)
            || (Math.round(step) !== step)
        ) {
            throw new Error("Range parameters must be integers.");
        }

        this._start = start;
        this._end = end;
        this._step = step;
        /** @type {Array<number>} */
        this._numbers = [];

        for (let i = start; i < end; i += step) {
            this._numbers.push(i);
        }
        if (this._numbers[this._numbers.length - 1] !== end) {
            this._numbers.push(end);
        }
    }

    /**
     * @returns {number}
     */
    get start() {
        return this._start;
    }

    /**
     * @returns {number}
     */
    get end() {
        return this._end;
    }

    /**
     * @returns {number}
     */
    get step() {
        return this._step;
    }

    /**
     * @returns {Array<number>}
     */
    get numbers() {
        return this._numbers;
    }
}

/**
 * Creates a new Range object with the given start value.
 *
 * @param {number} newStart
 * @param {Range} range
 */
function setStart(newStart, range) {
    return new Range({start: newStart, end: range.end, step: range.step});
}

/**
 * Creates a new Range object with the given end value.
 *
 * @param {number} newEnd
 * @param {Range} range
 */
function setEnd(newEnd, range) {
    return new Range({start: range.start, end: newEnd, step: range.step});
}

/**
 * Creates a new Range object with the given step value.
 *
 * @param {number} newStep
 * @param {Range} range
 */
function setStep(newStep, range) {
    return new Range({start: range.start, end: range.end, step: newStep});
}

export default Range;

export {
    Range,
    setStart,
    setEnd,
    setStep
}