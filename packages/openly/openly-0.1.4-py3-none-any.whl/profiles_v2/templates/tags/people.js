var tag = this;
tag.add_disabled = false;
tag.creating_empty_person = false;
tag.upload_url = opts.upload_url;
tag.csrf_token = opts.csrf_token;

// Add mixins: FileUploadMixin for a person's photo and SerializerMixin to communicate
// with the data store
tag.mixin(new FileUploadMixin(tag, function(response) {
    tag.person_data.photo = response.image
    tag.update()
}));
tag.mixin('SerializerMixin');
tag.all_people = tag.store[tag.store.el].sort(
    function(p1, p2) { return p1.order > p2.order; }
);
tag.people = [];
tag.mixin(new ExpandMixin(tag, 'people', 'all_people', 4));

tag.profile_pk = opts.profile_pk
tag.person_data = new Object();
tag.valid = true;

// Provide a handle, reorder the people array, and then update their ordering on the backend
var sortableOptions = {
    handle: '.icon-move',
    draggable: 'person',
    onEnd: function(e) {
        tag.all_people.splice(e.newIndex, 0, tag.all_people.splice(e.oldIndex, 1)[0]);
        tag.reorder_people();
    }
}

this.on('mount', function() {
    // Setup for file uploads
    tag.upload_container_selector = '#person-photo';
    tag.form_id = '#person-photo';
    tag.hide_file_input();

    // Get the organisation's people from the data store and display
    if (tag.all_people.filter(function(p) { return p.name == ''; }).length == 0) {
        tag.add_disabled = true;
        tag.create_empty_person()
    }
    tag.update();
    if (opts.editor) Sortable.create($('[ref="organisation_people_container"]')[0], sortableOptions);
});

tag.store.on(tag.store.requestopts.create_done, function(data, returned_data) {
    // Add person to local copy of data
    tag.all_people.push(returned_data);
    tag.add_disabled = false;
    tag.creating_empty_person = false;
    tag.update();
});

tag.store.on(tag.store.requestopts.update_done, function(data, returned_data) {
    // Find person in local data and if this was the "empty" person create a new empty person
    var person = _.find(tag.all_people, function(p) { return p.id == returned_data.id; });
    var index = _.indexOf(tag.all_people, person);
    if (person.name == '' && returned_data.name != '') {
        tag.add_disabled = true;
        tag.update();
        tag.create_empty_person();
    }

    // We have to copy all attributes because just copying the data directly updates only
    // this person tag pushing them to the end of the displayed list
    for (var k in returned_data) tag.all_people[index][k] = returned_data[k];
    tag.update_display();
});

tag.store.on(tag.store.requestopts.delete_done, function(data, returned_data) {
    // Because updates go through the SerializerMixin and NOT StoreMixin we need to manuallyl
    // inform the store that a person has been deleted
    tag.store.deleted(data);
    tag.all_people = tag.all_people.filter(function(p) { return p.id != data.id; })
    tag.update_display();
    tag.reorder_people();
});

add_person() {
    // Do a deep copy of the data so that if discarded we haven't changed the "real" copy
    tag.person_data = _.cloneDeep(_.find(tag.all_people, function(p) { return p.name == ''; }));
    tag.valid = true;
    tag.name_validation_message = '';
    tag.email_validation_message = '';
    tag.phone_number_validation_message = '';
    tag.update();
}

edit_person(person) {
    tag.valid = true;
    tag.person_data = _.cloneDeep(_.find(tag.people, function(p) { return p.id == person.id; }));
    tag.person_data.photo = person.photo;
    tag.name_validation_message = '';
    tag.email_validation_message = '';
    tag.phone_number_validation_message = '';
    tag.update();
    $('#person-modal').modal('show');
}

// Functions handling editing and validation

edit_name(e) {
    tag.person_data.name = e.target.value;
    if (tag.name_validation_message != '') tag.validate();
}

valid_name() {
    if (!('name' in tag.person_data) || tag.person_data.name == '') {
        tag.valid = false;
        tag.name_validation_message = 'Please include a name';
    } else {
        tag.name_validation_message = '';
        tag.valid = (tag.phone_number_validation_message == '' && tag.email_validation_message ==     '' && tag.name_validation_message == '');
    }
    tag.update();
}

edit_position(e) {
    tag.person_data.position = e.target.value;
}

edit_phone_number(e) {
    tag.person_data.phone_number = e.target.value;
    if (tag.phone_number_validation_message != '') tag.validate();
}

var phone_re = new RegExp(/^[\s()+-]*([0-9][\s()+-]*){6,20}$/);
valid_phone_number() {
    var ph = tag.person_data.phone_number;
    if (ph != null && ph != '' && typeof(ph) != 'undefined' && !phone_re.test(ph)) {
        tag.valid = false;
        tag.phone_number_validation_message = 'Must be a valid phone number';
    } else {
        tag.phone_number_validation_message = '';
        tag.valid = (tag.phone_number_validation_message == '' && tag.email_validation_message == '' && tag.name_validation_message == '');
    }
    tag.update()
}

edit_email(e) {
    tag.person_data.email = e.target.value;
    if (tag.email_validation_message != '') tag.validate();
}

valid_email() {
    var re = /^([a-zA-Z_\-0-9\.]+@[a-zA-Z_\-0-9\.]+\.[a-zA-Z]+)?$/
    if (tag.person_data.email != null && typeof(tag.person_data.email) != 'undefined' && !re.test(tag.person_data.email)) {
        tag.valid = false;
        tag.email_validation_message = 'The above email address is not valid';
    } else {
        tag.email_validation_message = '';
        tag.valid = (tag.phone_number_validation_message == '' && tag.email_validation_message == '' && tag.name_validation_message == '');
    }
    tag.update();
}

validate() {
    tag.valid_name();
    tag.valid_email();
    tag.valid_phone_number();
    tag.valid = (tag.phone_number_validation_message == '' && tag.email_validation_message == '' && tag.name_validation_message == '');
    tag.update();
}

save_person() {
    if ('id' in tag.person_data) {
    	delete tag.person_data.photo;
    	tag.put(tag.person_data, _.extend(tag.store.requestopts,
    					  {method: 'PATCH',
    					   update: tag.store.urls().get_update_url(tag.person_data['id'])}));
    } else {
        tag.post(tag.person_data, tag.store.requestopts);
    }
}

delete_person() {
    tag.delete(tag.person_data, _.extend(tag.store.requestopts,
                                         {method: 'DELETE',
                                             delete: tag.store.urls().get_update_url(tag.person_data['id'])}));
}

reorder_people() {
    tag.all_people.forEach(function(person, index) {
	person['order'] = index;
	delete person.photo;
	tag.put(person, _.extend(tag.store.requestopts,
				 {method: 'PATCH',
				  update: tag.store.urls().get_update_url(person['id'])}));
    });
    tag.update_display();
}

create_empty_person() {
    if (!tag.creating_empty_person) {
        tag.creating_empty_person = true;
        tag.person_data = tag.new_person_data = new Object({
            is_hamutuk_contact: false,
            name: '',
            organisation_profile: tag.profile_pk,
            order: tag.all_people.length,
        });
        tag.save_person();
    }
}

$(function() {
    $('[data-toggle="popover"]').popover();
});
