    var tag = this;
    var parent = tag.parent;
    tag.opts.store = parent.store;
    tag.store = parent.store;
    tag.reasons = []; // Why are we showing this tag, bool[]
    tag.show = undefined;
    tag.hide = undefined;

    function getParentState() {
        /* Run 'get_validation_state' on parent tag */
        /* Returns an object with properties of interest about the parent's state */
        var validation_state = _.invoke(parent, 'get_validation_state', parent);
        if (_.get(tag, 'parent.opts.ValidationMixin.show_as_changed')) {
            validation_state.changed = true;
        }
        return validation_state;
    }

    function getReasons() {
        /* Array of tests about whether we show the error(s) or not */
        /* Any "true" value indicates a displayed error */
        var validation_state = getParentState();
        var changed = !_.isEqual(validation_state.initial, validation_state.value);
        var tests = [
            _.isEqual(parent.errors, {}), // Parent has no errors
            validation_state.validated === true,  // Parent is validated
            (!_.isUndefined(tag.opts.only_if_unchanged)) && changed, // And the value changeTag is for changed values and there are changes
            (!_.isUndefined(tag.opts.only_if_changed)) && !changed // Or tag is for changed values, and the value has not changes
        ];
        return tests;
    }

    function setShowState() {
        var update;
        var shouldHide;
        tag.reasons = getReasons();
        shouldHide = _.includes(tag.reasons, true);
        update = { hide: shouldHide, show: !shouldHide };
        if (tag.show !== update.show) { tag.update(update); }
    }

    tag.on('mount', setShowState);
    tag.on('update', setShowState);
