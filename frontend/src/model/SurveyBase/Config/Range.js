import * as R from "ramda";

class Range {
  /**
   * @param {number} start
   * @param {number} end
   * @param {string} startLabel
   * @param {string} endLabel
   */
  constructor({ start = 0, end, startLabel, endLabel }) {
    if (start > end) {
      throw new Error("Range start can't be bigger than end.");
    }
    if (Math.round(start) !== start || Math.round(end) !== end) {
      throw new Error("Range parameters must be integers.");
    }

    this._start = start;
    this._end = end;
    this._startLabel = startLabel;
    this._endLabel = endLabel;
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
    if (newStart >= this._end) {
      throw new Error("Start must be smaller than end.");
    }
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
    if (newEnd <= this._start) {
      throw new Error("End must be bigger than start.");
    }
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
   * Getter for startLabel.
   * @returns {string}
   */
  get startLabel() {
    return this._startLabel;
  }

  /**
   * Getter for endLabel.
   * @returns {string}
   */
  get endLabel() {
    return this._endLabel;
  }

  /**
   * @returns {Array<number>}
   */
  get numbers() {
    return this._numbers;
  }

  /**
   *
   * @returns {number}
   */
  get span() {
    return this._end - this._start + 1;
  }

  /**
   * @returns {Range}
   */
  clone() {
    return new Range({
      start: this._start,
      end: this._end,
      startLabel: this._startLabel,
      endLabel: this._endLabel
    });
  }

  /**
   * Strict equality check.
   *
   * @param {Range} otherRange
   * @returns {Boolean}
   */
  equals(otherRange) {
    return R.allPass([
      o => R.equals(o.start, this.start),
      o => R.equals(o.end, this.end),
      o => R.equals(o.startLabel, this.startLabel),
      o => R.equals(o.endLabel, this.endLabel)
    ])(otherRange);
  }
}

export default Range;

export { Range };
