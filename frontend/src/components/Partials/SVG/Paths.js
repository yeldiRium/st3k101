/**
 * Creates SVG Path for a rounded diamond.
 * @param width
 * @param height
 * @param radius
 * @param {int} x
 * @param {int} y
 * @returns {string}
 */
const roundedDiamond = function (width, height, radius, x=0, y=0) {
    width = parseInt(width);
    height = parseInt(height);
    radius = parseInt(radius);
    x = parseInt(x);
    y = parseInt(y);
    let out = `M${x + 0.5 * width + radius},${y + radius}`;

    out += ` L${x + width - radius},${y + 0.5 * height - radius}`;
    out += ` Q${x + width},${y + 0.5 * height} ${x + width - radius},${y + 0.5 * height + radius}`;

    out += ` L${x + 0.5 * width + radius},${y + height - radius}`;
    out += ` Q${x + 0.5 * width},${y + height} ${x + 0.5 * width - radius},${y + height - radius}`;

    out += ` L${x + radius},${y + 0.5 * height + radius}`;
    out += ` Q${x},${y + 0.5 * height} ${x + radius},${y + 0.5 * height - radius}`;

    out += ` L${x + 0.5 * width - radius},${y + radius}`;
    out += ` Q${x + 0.5 * width},${y} ${x + 0.5 * width + radius},${y + radius}`;

    return `${out} Z`;
};

export {
    roundedDiamond
};