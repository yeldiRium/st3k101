const atLeastZero = a => a >= 0;

const between = function (a, b) {
    return function (x) {
        return a <= x && x <= b;
    };
};

const hexColorValidator = function (hexColor) {
    return hexColor.match(/^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/) !== null;
};

export {
    atLeastZero,
    between,
    hexColorValidator
};