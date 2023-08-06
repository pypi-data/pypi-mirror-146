/* globals gettext, accounting */
/* Requires the 'accounting.js' library */
/* Extends the 'accounting.js' library with more compact number representation */

/* Stub 'gettext' if it does not exist */
var gettext = window.gettext || function () { return undefined; };
var _gettext = function(text){
    // Wrapper to prevent returning the same text string - thie can break when 'billion marker' is not defined in gettesxt lookup
    var gottext = gettext(text)
    if (gottext && gottext != text){return gottext}
}
/**
 * Return the input number divided by some thousands and a unit indicator
 * @param amt
 * @returns {{amt: *, units: *}}
 */
function prettify_compact(amt) {
    var n;
    var units;
    if (amt >= 1e12) {
        n = amt / 1e12;
        units = _gettext('trillion_marker') || 'T';
    } else if (amt >= 1e9) {
        n = amt / 1e9;
        units = _gettext('billion_marker') || 'B';
    } else if (amt >= 1e6) {
        n = amt / 1e6;
        units = _gettext('million_marker') || 'M';
    } else if (amt >= 1e3) {
        n = amt / 1e3;
        units = _gettext('thousand_marker') || 'K';
    } else {
        amt = n;
        units = '';
    }
    return { amt: n, units: units };
}
function compact_format_money(value, sign, digits) {
    var compact;
    if (!(accounting.compact_money_format)) {
        return accounting.formatMoney(value, sign || '$', digits || 2);
    }
    compact = prettify_compact(value);
    return accounting.formatMoney(compact.amt, sign || '$', digits || 1) + compact.units;
}
// Extends 'accounting[.min].js'
accounting.compactFormatMoney = compact_format_money;
accounting.compact_money_format = true;
