var tag = this;
tag.mixin('SerializerMixin');
tag.contact_info = new Object()
tag.new_contact_info = new Object()

this.on('mount', function() {
    tag.contact_info = tag.store[tag.store.el];
    tag.update();
});

tag.store.on(tag.store.requestopts.update_done, function(data, returned_data) {
    tag.contact_info = returned_data;
    tag.update();
});

init_modal_values() {
    tag.valid = true
    for (key in tag.contact_info) {
        tag.new_contact_info[key] = tag.contact_info[key]
    }
    tag.phone_number_validation_message = ''
    tag.fax_validation_message = ''
    tag.email_validation_message = ''
    tag.website_validation_message = ''
    tag.facebook_validation_message = ''
    tag.twitter_validation_message = ''
}

save_contact_info(e) {
    tag.put(tag.new_contact_info, _.extend(tag.store.requestopts, {method: 'PATCH'}));
}

edit_address(e) {
    tag.new_contact_info.address = e.target.value;
}

edit_phone_number(e) {
    tag.new_contact_info.phone_number = e.target.value;
    if (tag.phone_number_validation_message != '') tag.valid_phone_number();
}

valid_phone_number() {
    var re = new RegExp(/^((?:(?:\+)[0-9]{2,3})([.-\s])?([0-9]{6,12}))(([.-\s])?(([EXText]){1,3}[.\s]?[0-9]{1,5}))?$/);
    // removed org phone validation check but leaving overall framework in place.
    // if (tag.new_contact_info.phone_number != null && !re.test(tag.new_contact_info.phone_number)) {
    //     tag.valid = false;
    //     tag.phone_number_validation_message = 'Must be a valid Timor phone number';
    // } else {
    tag.phone_number_validation_message = '';
    tag.valid = (tag.phone_number_validation_message == '' && tag.email_validation_message == '' && tag.website_validation_message == '');
    // }
    tag.update()
}

edit_fax(e) {
    tag.new_contact_info.fax = e.target.value;
    if (tag.fax_validation_message != '') tag.valid_fax();
}

valid_fax() {
    var re = new RegExp(/^((?:(?:\+)[0-9]{2,3})([.-\s])?([0-9]{6,12}))(([.-\s])?(([EXText]){1,3}[.\s]?[0-9]{1,5}))?$/);
    // removed org phone validation check but leaving overall framework in place.
    // if (tag.new_contact_info.fax != null && !re.test(tag.new_contact_info.fax)) {
    //     tag.valid = false;
    //     tag.fax_validation_message = 'Must be a valid Timor phone number';
    // } else {
    tag.fax_validation_message = '';
    tag.valid = (tag.fax_validation_message == '' && tag.email_validation_message == '' && tag.website_validation_message == '');
    // }
    tag.update()
}

edit_email(e) {
    tag.new_contact_info.email = e.target.value;
    if (tag.email_validation_message != '') tag.valid_email();
}

valid_email() {
    var re = /^([a-zA-Z_\-0-9\.]+@[a-zA-Z_\-0-9\.]+\.[a-zA-Z]+)?$/
    if (tag.new_contact_info.email != null && !re.test(tag.new_contact_info.email)) {
        tag.valid = false;
        tag.email_validation_message = 'Email address is invalid!';
    } else {
        tag.email_validation_message = '';
        tag.valid = (tag.phone_number_validation_message == '' && tag.email_validation_message == '' && tag.website_validation_message == '');
    }
    tag.update();
}

edit_website(e) {
    tag.new_contact_info.website = e.target.value;
    if (tag.website_validation_message != '') tag.valid_website();
}

valid_website() {
    var re = /^((https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*))?$/;
    if (tag.new_contact_info.website != null && !re.test(tag.new_contact_info.website)) {
        tag.valid = false;
        tag.website_validation_message = 'Website address is invalid!';
    } else {
        tag.website_validation_message = '';
        if (tag.new_contact_info.website != null && tag.new_contact_info.website.slice(0,4) != 'http') {
            tag.new_contact_info.website = 'http://' + tag.new_contact_info.website
        }
        tag.valid = (tag.phone_number_validation_message == '' && tag.email_validation_message == '' && tag.website_validation_message == '');
    }
    tag.update();
}

// TODO: Figure out what sort of validation we need to do on facebook/twitter accounts
edit_facebook(e) {
    tag.new_contact_info.facebook = e.target.value;
}

valid_facebook() {
}

edit_twitter(e) {
    tag.new_contact_info.twitter = e.target.value;
}

valid_twitter() {
}

validate() {
    tag.valid_phone_number();
    tag.valid_fax();
    tag.valid_email();
    tag.valid_website();
    tag.valid = (tag.phone_number_validation_message == '' && tag.email_validation_message == '' && tag.website_validation_message == '' && tag.facebook_validation_message == '' && tag.twitter_validation_message == '');
    tag.update();
}

window.twttr = (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0],
        t = window.twttr || {};
        if (d.getElementById(id)) return t;
        js = d.createElement(s);
        js.id = id;
        js.src = "https://platform.twitter.com/widgets.js";
        fjs.parentNode.insertBefore(js, fjs);

        t._e = [];
        t.ready = function(f) {
            t._e.push(f);
        };

        return t;
}(document, "script", "twitter-wjs"));
