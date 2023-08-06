    /*
    It's Dangerous to do this!
    A classic "Are you REALLY sure?" modal
     */

    var tag = this;
    var defaults = {
        title: 'Are you sure?',
        content: 'This will remove something permanently',
        show: true
    };

    tag.on('update', function () {
        if (tag.opts.show === true) {
            $('.modal', tag.root).modal('show');
        }
        if (tag.opts.show === false) {
            $('.modal', tag.root).modal('hide');
        }
    });

    tag.nope = function () {
        tag.opts.show = false;
        if (_.isFunction(tag.opts.cancel)) {
            tag.opts.cancel();
        }
    };

    tag.yolo = function () {
        tag.opts.show = false;
        if (_.isFunction(tag.opts.confirm)) {
            tag.opts.confirm();
        }
    };


    RiotControl.on('confirm-delete', function (opts) {
        tag.update({ opts: _.defaults(opts, defaults) });
    });
