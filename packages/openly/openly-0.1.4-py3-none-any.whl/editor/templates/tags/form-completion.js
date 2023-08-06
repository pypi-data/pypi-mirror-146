var tag = this;

function store() { return stores.activityStore; }
function activity() { return store().activity; }
function reload_completion(data) {
    tag.update({
        tasks: data.completion_tasks,
        completion_percentage: data.completion_percentage
    });
}

tag.store = store();
tag.activity = activity();

tag.mixin('SerializerMixin');

tag.on('mount', function () {
    reload_completion(activity());
    $('#activity-completion-help').popover();
});

RiotControl.on('activity_updated', function () { reload_completion(activity()); });
RiotControl.on('update_activity_completion', function (activity_data) { reload_completion(activity_data); });
