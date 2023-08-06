function PeopleStore(api_endpoint, organisation_pk, organisation_profile_pk, token, people) {
    var store = this;
    if (typeof(people) != 'undefined') {
	store.data = people;
    } else {
	store.data = new Object();
    }
    riot.observable(this);
    store.fetching_data = false;

    this.get_people = function() {
	if (store.fetching_data) return;

	if (!jQuery.isEmptyObject(store.data)) {
	    RiotControl.trigger('people_available', store.data);
	}

	store.fetching_data = true;
	$.ajax({
	    url: api_endpoint,
	    type: 'GET',
	    data: { organisation_pk: organisation_pk },
	    success: function(data, _, xhr) {
		if (xhr.status == 200) {
		    store.data = data
		    RiotControl.trigger('people_available', store.data);
		}
	    },
	    done: function() {
		store.fetching_data = false;
	    }
	});
    }

    this.save_person = function(person_data) {
	delete person_data.photo;
	if ('id' in person_data) {
	    this.update_person(person_data['id'], person_data);
	} else {
	    this.add_person(person_data);
	}
    }

    this.save_people = function(people) {
	let requests = people.map((person) => {
	    delete person.photo;
	    return new Promise((resolve) => {
		this.update_person(person['id'], person, resolve);
	    });
	})

	Promise.all(requests).then(() => {
	    store.data.sort(function(p1, p2) { return p1.order - p2.order; });
	    RiotControl.trigger('people_available', store.data);
	});
    }

    this.add_person = function(person_data) {
	person_data['organisation_profile'] = organisation_profile_pk;
	$.ajax({
	    url: api_endpoint,
	    method: 'POST',
	    headers: {'X-CSRFTOKEN': csrf_token},
	    data: person_data,
	    success: function(data, _, xhr) {
		store.data.push(data);
		RiotControl.trigger('people_available', store.data)
	    },
	});
    }

    this.update_person = function(person_id, person_data, cb = function() { RiotControl.trigger('people_available', store.data); }) {
	$.ajax({
	    url: api_endpoint + person_id + '/',
	    method: 'PATCH',
	    headers: {'X-CSRFTOKEN': csrf_token},
	    data: person_data,
	    success: function(data, _, xhr) {
		for (idx in store.data) {
		    person = store.data[idx];
		    if (person.id == person_id) {
			store.data[idx] = data;
			cb();
			break;
		    }
		}
	    },
	});
    }

    this.delete_person = function(person_id) {
	$.ajax({
	    url: api_endpoint + person_id + '/',
	    method: 'DELETE',
	    headers: {'X-CSRFTOKEN': csrf_token},
	    success: function() {
		store.data = store.data.filter(function(p) { return p.id != person_id; });
		RiotControl.trigger('people_available', store.data);
	    }
	});
    }
}
