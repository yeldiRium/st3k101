class Range {
    /**
     * @param {number} start
     * @param {number} end
     */
    constructor({start = 0, end}) {
        if (start > end) {
            throw new Error("Range start can't be bigger than end.");
        }
        if (
            (Math.round(start) !== start)
            || (Math.round(end) !== end)
        ) {
            throw new Error("Range parameters must be integers.");
        }

        this._start = start;
        this._end = end;
        /** @type {Array<number>} */
        this._numbers = [];
        this.calcNumbers();
    }

    /**
     * Calculates the exact number range.
     */
    calcNumbers() {
        this._numbers = [];
        for (let i = this._start; i <= this._end; i++) {
            this._numbers.push(i);
        }
    }

    /**
     * Recalculates numbers when setting start value.
     * @param {number} newStart
     */
    set start(newStart) {
        this._start = Math.floor(newStart);
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
        this._end = Math.floor(newEnd);
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