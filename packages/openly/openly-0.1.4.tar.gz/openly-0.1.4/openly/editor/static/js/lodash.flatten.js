/* eslint vars-on-top: 0, guard-for-in: 0,
no-restricted-syntax: 0, no-cond-assign:0, block-scoped-var:0 , func-names:0*/
// Some legacy code here is not comptible yet with eslint hence exceptions above
_.mixin({
  /**
   * Returns the sum of integer values of the given path regex
   * @param data
   * @param regular_expression
   * @returns {int}
   */
    sumOfPaths: function (data, regular_expression) {
        var fields = _(data)
        .objectflatten()
        .filterPathWithRegex(regular_expression);

        var sum = fields
        .map(_.toInteger)
        .sum();
        return {
            fields: fields.value(),
            result: sum
        };
    },

    sumOfPathsIsPercentage: function (data, regular_expression) {
        var result = _.sumOfPaths(data, regular_expression);
        result.passed = (result.result === 100);
        return result;
    },

    pathsUnique: function (data, regular_expression) {
        var fields = _(data)
        .objectflatten()
        .filterPathWithRegex(regular_expression)
        .value();

        return {
            fields: fields,
            passed: _(fields).isEqual(_.uniq(fields))
        };
    },

    getWithRegularExpression: function (data, regular_expression) {
        return _(data).objectflatten()
        .filterPathWithRegex(regular_expression);
    },

  /**
   * Filter an object returning paths matching a regex
   * @param data
   * @param exp
   * @returns {*}
   */
    filterPathWithRegex: function (data, exp) {
        return _.filter(_.objectflatten(data), function (value, key) {
            return exp.test(key);
        });
    },

  /**
   * Return a hierarchy (i.e. a standard Object)
   * @param data
   * @returns {*}
   */
    objectunflatten: function (data) {
        if (Object(data) !== data || Array.isArray(data)) {
            return data;
        }

        var regex = /\.?([^.\[\]]+)|\[(\d+)\]/g;
        var resultholder = {};
        for (var p in data) {
            var cur = resultholder;
            var prop = '';
            var m;
            while (m = regex.exec(p)) {
                cur = cur[prop] || (cur[prop] = (m[2] ? [] : {}));
                prop = m[2] || m[1];
            }

            cur[prop] = data[p];
        }

        return resultholder[''] || resultholder;
    },

    /**
     * Return an array of "flattened" JSON data
     * @param data
     * @returns {*}
     */
    objectflatten: function (data) {
        var result = {};

        function recurse(cur, prop) {
            if (Object(cur) !== cur) {
                result[prop] = cur;
            } else if (Array.isArray(cur)) {
                for (var i = 0, l = cur.length; i < l; i += 1) {
                    recurse(cur[i], prop + '[' + i + ']');
                }

                if (l === 0) {
                    result[prop] = [];
                }
            } else {
                var isEmpty = true;
                for (var p in cur) {
                    isEmpty = false;
                    recurse(cur[p], prop ? prop + '.' + p : p);
                }

                if (isEmpty && prop) {
                    result[prop] = {};
                }
            }
        }

        recurse(data, '');
        return result;
    }
});
