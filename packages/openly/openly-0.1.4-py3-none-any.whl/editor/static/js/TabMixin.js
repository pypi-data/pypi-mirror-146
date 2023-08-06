/* global _ routeToTag */
/* eslint no-underscore-dangle: 0, no-param-reassign: 0 */
/* exported TabMixin */

var TabMixin;

function setWindowTab(tag) {
    /* Check that expected functions are present on the tag */
    _.each(['save', 'discard'], function (methodName) {
        if (!_.isFunction(_.get(tag, methodName))) {
            // console.warn('Devs: Please add this function to the tag', methodName, tag);
        }
    });

    (function () {
        window.current_tab = {
            tab: tag,
            enableRouting: function () {
                return !tag.has_changed();
            }
        };
    }(window));
}

TabMixin = {
    /** A set of methods used when the user tries to navigate away from the current tab.
     *
     * Expected existing tag properties:
     *   - store object, with the `_initial` object property and `load_data` method
     *   - serialize_object method
     */

    init: function () {
        var tag = this;
        tag.on('updated', function () {
            var current_tag;
            var current_tag_link;
            current_tag_link = window.location.hash || $('form-navigation li.active a').attr('href') || '#general';
            current_tag_link = current_tag_link.slice(1, current_tag_link.length); // strip the leading '#'
            current_tag = document.querySelector('[route="' + current_tag_link + '"]');
            if (!current_tag) { return; } /* This happens when we are on an "unexpected" URL - either an error or results tab subrouter */
            current_tag = current_tag._tag;
            if (current_tag === tag && _.isFunction(tag.validate)) {
                tag.validate();
            }
        });

        this.on('route', function () {
            setWindowTab(this);
            this.on('updated', function () {
                setWindowTab(this);
            });
        });
    },

    validate_with_children: function () {
        var tag = this;
        var initial_value = tag.validated_with_children;
        if (!_.isFunction(tag.validate)) {
            // ex: default settings tab
            return true;
        }
        if (_.isFunction(tag.child_tags_validated)) {
            /* Dev - might want to check this */
            console.warn('A tag is missing validated_with_children function', tag); // eslint-disable-line no-console
            tag.validated_with_children = tag.validate() && tag.child_tags_validated();
        } else {
            tag.validated = tag.validate();
        }
        if (initial_value !== tag.validated_with_children) {
            tag.update();
        }
        return tag.validated_with_children;
    },

    next: function () {
        /* Called when the user clicks the "Next" button. */
        var tag = this;
        var modal_opts;
        if (tag.has_changed()) {
            // Here, we want to trigger the "save or discard?" modal
            modal_opts = {
                show: true,
                current_tag: window.current_tab,
                route: routeToTag.getNext()
            };
            $('discard-modal')[0]._tag.update({ opts: modal_opts });
        } else {
            routeToTag.next();
        }
    },

    has_changed: function () {
        /** DEPRECATED FUNCTION
         * Better set on each individual tag
         * Return whether the current tab data is different than the initial data.
         * In other words, whether hitting "Save" would change anything in the database.
         */
        var tag = this;
        var current;

        function object_contains(larger_object, smaller_object) {
            /** For each entry in smaller_object, check that the larger_object has the same entry.
             * If the entry is itself an object, recurse.
             *
             * For array inputs, this function will return false when the arrays are not of the same size.
            * */
            var larger_value;
            if (!_.isObject(smaller_object)) {
                if (Boolean(smaller_object) === false && Boolean(larger_object) === false) {
                    // ex: consider null and '' equivalent
                    return true;
                }
                if (_.isString(smaller_object)) {
                    // trim strings, unify the new line characters
                    smaller_object = _.trim(smaller_object).replace(/(\r\n|\n|\r)/gm);
                    larger_object = _.trim(larger_object).replace(/(\r\n|\n|\r)/gm);
                }
                return smaller_object === larger_object;
            } else if (_.isArray(smaller_object) && larger_object.length > smaller_object.length) {
                return false;
            }
            return _.every(smaller_object, function (smaller_value, key) {
                if (larger_object === undefined || larger_object === null) {
                    return false;
                }
                larger_value = larger_object[key];
                return object_contains(larger_value, smaller_value);
            });
        }
        if (_.isFunction(tag.serialize_object)) {
            current = tag.serialize_object();
            return !object_contains(tag.store._initial, current);
        }
        return false;
    }
};
