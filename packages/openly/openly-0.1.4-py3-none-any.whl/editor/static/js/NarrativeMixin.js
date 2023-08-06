
var NarrativeMixin = {

    /** get_filter returns an object to use to search for existing narrative-to-object through models such as ResultTitle
     *  Example
     *  <my-tag result="{result}" content_type="result" narrated_model="result" content_type="resulttitle">
     *      Returns {result: 15 content_type: 'result_title'}
     *      This is expected to have a "narratives" property attached to it which is a list of serialized aims_narrative
     * */
    get_filter: function get_filter() {
        var filter = {content_type: this.opts.content_type}; /* content_type would be eg 'result_title' */
        filter[this.opts.narrated_model] = this.opts[this.opts.narrated_model].id;
        return filter;
    },

    /** get the related content object */
    get_related: function get_related(){return _.find(stores.resultsStore.results, this.get_filter())},

    /** return the "narratives" property of the through model */
    get_narratives: function get_narratives() {return _.get(this.get_related(), 'narratives', []);},
    add_narrative: function add_narrative() {
        var tag = this;
        /**
         * push_title creates a stub for missing title object with a "Narratives" array
         **/
        function push_related() {
            if (tag.get_related()){return}
            var filter = tag.get_filter();
            filter.narratives = [];
            stores.resultsStore.results.push(filter);
        }

        /**
         * push_narrative creates a new empty array on the get_title() objects' narrative property
         **/
        function push_narrative(){
            var related_object_data = {};
            related_object_data[tag.opts.narrated_model+'_id'] = tag.opts[tag.opts.narrated_model].id; /* Add for example a result id */
            push_related();
            tag.get_narratives().push({
                content: "",
                language: tag.opts.language || 'en', /* Not implemented yet: Multiple languages */
                /* the following parameters provide instructions for the NarrativeViewSet to create a new ResultTitle if one does not exist */
                model: tag.opts.content_type,
                related_object_data: related_object_data
            });
        }
        push_narrative();
        this.update_narratives();
    },

    update_narratives: function update_narratives(){
        var tag = this;
        var narratives = tag.get_narratives();
        if (!_.isEqual(narratives, tag.narratives)){
            tag.update({narratives:narratives})
        }
    },

    /** When a Narratvie is removed a 'removed_narrative' trigger is fired. Here we remove the narrative  __from the object__
     * Note the handling is a little different to our other models which remove from "stores.resultsStore.results".
     * @param id
     */
    on_resultStore_removed: function on_resultsStore_removed(id){
        var tag = this;

        if (_.find(tag.narratives, {id:id})) {
            _.remove(tag.get_related().narratives, {id:id});
            tag.update_narratives();
            tag.parent.update();
        }
    },

    init: function init(opts) {

        this.on('mount', function () {
            var tag = this;
            /* Ensure that this tag has the required opts:
            *  an object for actioning, an object name which ought to correspond to the key of the opt,
            *  and optionally a lang code
            * */
            stores.resultsStore.on('removed_narrative', this.on_resultStore_removed)
        });
        this.on('unmount', function () {
            var tag = this;
            stores.resultsStore.off('removed_narrative', this.on_resultStore_removed)
        });


        this.on('mount', function () {
            this.update_narratives();
            if (_.size(this.narratives) === 0) {
                this.add_narrative();
            }


        });
        this.on('update', function () {
            this.update_narratives();
            if (_.size(this.narratives) === 0)  {
                this.add_narrative();
            }
        });
    }
};
    
riot.mixin('NarrativeMixin', NarrativeMixin);


var NarrativeFieldMixin = {

    init: function () {
        var tag = this;

        tag.on('mount', function () {
            stores.resultsStore.on('updated', tag.oninput);

            tag.on('update_if_changed', function () {
                /* Early-out if we are readonly */
                if (tag.opts.readonly){return}
                var has_changed = tag.opts.narrative.content !== tag.refs.content.value;
                if (tag.has_changed !== has_changed) {
                    tag.update({has_changed: has_changed})
                }
            });

        });

        tag.on('unmount', function () {
            stores.resultsStore.off('updated', tag.oninput);
            tag.off('update_if_changed');
        });
    },
    /**
     * This mixin is for a "Narrative Editor" - type field or fields
     */

    oninput: function () {
        var tag = this;
        tag.trigger('update_if_changed')
    },

    /**
     * Make the request for saving this object
     * @param e
     * @returns {boolean}
     */
    save_narrative: function (e) {
        var tag = this;

        /* Rather than calling preventDefault directly, lodash's "invoke" function will play nicely when we
        * call this from anything other than an 'event' type
        * */
        _.invoke(e, 'preventDefault');

        /**
         * Generate data for saving this object
         */
        get_data = function get_data() {
            /* Clone the data, don't update directly or we may end up in an unclear state if the save fails */
            var data = _.clone(tag.opts.narrative);
            /* Set 'ref' names on fields to be appended to this data - content and language */
            _.assign(data, _.mapValues(tag.refs, 'value'));
            /* An activity id is a required field for a Narrative */
            data.activity = stores.activityStore.activity.id;
            return data
        };

        /*  */
        stores.resultsStore.make_request({object_type: 'narrative', data: get_data(), assign: tag.opts.narrative});
        return false;
    },

    /**
     * Delete this narrative
     */
    delete_narrative: function delete_narrative(e) {
        /* Rather than calling preventDefault directly, lodash's "invoke" function will play nicely when we
        * call this from anything other than an 'event' type
        * */
        _.invoke(e, 'preventDefault');
        stores.resultsStore.make_request({
            object_type: 'narrative',
            data: {id: this.opts.narrative.id},
            method: 'delete',
            assign: this.opts.narrative
        });
        return false;
    }
};

riot.mixin('NarrativeFieldMixin', NarrativeFieldMixin);