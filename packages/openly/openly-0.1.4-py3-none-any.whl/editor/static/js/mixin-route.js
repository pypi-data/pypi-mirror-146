/* global $ RiotControl riot stores route */
/* eslint no-underscore-dangle: 0 */
/* exported RouteableTriggerMixin RouteableListenerMixin */

var RouteableTriggerMixin = {
    // This mixin makes a change to the URL when a riot function is triggered

    init: function () {
        var tag = this;
        tag.opts.route_base = tag.opts.route_base || '';
        tag.list_items = tag.opts.list_items || [{ name: 'navigationlist', title: 'Navlist' }];
        tag.active = tag.list_items[0];
        tag.route = route.create();

        tag.on('mount', function () {
            RiotControl.on('route_tab', function (name) {
                tag.active = (_(tag.list_items).find({ name: name }) ||
                             _(tag.list_items).find({ name: name.split('/')[0] }) ||
                             _(tag.list_items).find(function (list_item) { return list_item.name.split('/')[0] === name.split('/')[0]; })
                             );
                tag.update();
            });
        });
    },

    tab: function (e) {
        /* Browses to the clicked tab. If the current tab has unsaved changes, a modal is shown. */
        var modal_opts;
        var current_tag;
        var current_tag_link = window.location.hash || $('form-navigation li.active a').attr('href') || '#general';

        e.preventDefault();
        current_tag_link = current_tag_link.slice(1, current_tag_link.length);  // strip the leading '#'
        current_tag = document.querySelector('tab-container [route="' + current_tag_link + '"]');

        // The selected tag should have a "route" property but if this is omitted change tags
        if (current_tag === null) {
            this.activate(e.item);
            return;
        }

        current_tag = current_tag._tag;
        if (e.item.name === current_tag_link) {
            return;
        }

        if (current_tag.has_changed() && !_.get(current_tag, 'opts.ValidationMixin.allow_tab_change')) {
            modal_opts = {
                show: true,
                current_tag: current_tag,
                clicked_tab: e.item.name
            };
            $('discard-modal')[0]._tag.update({ opts: modal_opts });
        } else {
            if (_.isFunction(current_tag.cancel) && current_tag.current_edit !== -1) {
                current_tag.cancel();
            }
            this.activate(e.item);
            $(current_tag.root).hide();
        }
    },

    activate: function (item) {
        this.active = item;
        route(this.opts.route_base + item.name);
        stores.activityStore.trigger('route_tab', this.opts.route_base + item.name);
    }

};


var RouteableListenerMixin = {
    // This mixin listens for changes to the URL and shows or hides different sub-tags based on their "route" property

    init: function () {
        var tag = this;
        tag.on('mount', function () {
            RiotControl.on('route_tab', function (route) {
                var show = false;
                var show_tag;
                $.each(tag.tags, function (i, sub_tag) {
                    if (sub_tag.opts.route === undefined) {
                        show = $(sub_tag.root).show();
                    } else if (route.indexOf(sub_tag.opts.route) === 0) {
                        // ex: route === 'all_finance' and sub_tag.opts.route === 'all_finance/transactions'
                        show = $(sub_tag.root).show();
                        window.banner_message.hide('warning');
                        show_tag = show[0]._tag;
                        show_tag.update();
                        if (_.isFunction(show_tag.validate)) {
                            show_tag.validate();
                        }
                    } else {
                        $(sub_tag.root).hide();
                    }
                });
                if (show === false) {
                    $.each(tag.tags, function (i, sub_tag) { if (show === false) { show = $(sub_tag.root).show(); } }); // By default show the first tab
                }
            });
        });

        tag.on('mount', function () {
            // Hide all sub tabs which have a "route" option
            $.each(tag.tags, function (i, sub_tag) {
                if (sub_tag.opts.route !== undefined) {
                    $(sub_tag.root).hide();
                }
            });
        });
    }
};
