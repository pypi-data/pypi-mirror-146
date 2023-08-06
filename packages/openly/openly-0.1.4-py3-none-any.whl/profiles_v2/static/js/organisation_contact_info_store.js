// current empty, but required to enable events
function ContactInfoStore(api_endpoint, token, contact_info) {
    var store = this;
    if (typeof(contact_info) != 'undefined') {
	store.data = contact_info
    } else {
	store.data = new Object();
    }
    riot.observable(this);
    store.fetching_data = false;

    this.get_contact_info = function() {
	if (store.fetching_data) return;
	
	if (!jQuery.isEmptyObject(store.data)) {
	    RiotControl.trigger('contact_info_available', store.data);
	}

	store.fetching_data = true;
        $.ajax({
            url: api_endpoint,
            type: 'GET',
            success: function(data, _, xhr) {
                if (xhr.status == 200) {
                    store.data = data;
                    RiotControl.trigger('contact_info_available', store.data);
                }
            },
	    done: function() {
		store.fetching_data = false;
	    }
        });
    }

    this.save_contact_info = function(contact_info) {
	$.ajax({
	    data: contact_info,
	    method: 'PATCH',
	    url: api_endpoint,
	    headers: {'X-CSRFTOKEN': token},
	    success: function(data, _, xhr) {
		store.data = data
		RiotControl.trigger('contact_info_available', store.data)
	    }
	});
    }
}
