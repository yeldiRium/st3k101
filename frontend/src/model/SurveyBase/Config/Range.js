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
        this.calcNumbers();
    }

    /**
     * Calculates the exact number range.
     */
    calcNumbers() {
        this._numbers = [];
        for (let i = this._start; i < this._end; i += this._step) {
            this._numbers.push(i);
        }
        if (this._numbers[this._numbers.length - 1] !== this._end) {
            this._numbers.push(this._end);
        }
    }

    /**
     * Recalculates numbers when setting start value.
     * @param {number} newStart
     */
    set start(newStart) {
        this._start = newStart;
        this.calcNumbers();
    }

    /**
     * Getter for start.
     * @returns {number}
     */
    get start() {
        return this._start;
    }

    /**
     * Recalculates numbers when setting end value.
     * @param {number} newEnd
     */
    set end(newEnd) {
        this._end = newEnd;
        this.calcNumbers();
    }

    /**
     * Getter for end.
     * @returns {number}
     */
    get end() {
        return this._end;
    }

    /**
     * Recalculates numbers when setting step value.
     * @param {number} newStep
     */
    set step(newStep) {
        this._step = newStep;
        this.calcNumbers();
    }

    /**
     * Getter for step.
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

export default Range;

export {
    Range
}