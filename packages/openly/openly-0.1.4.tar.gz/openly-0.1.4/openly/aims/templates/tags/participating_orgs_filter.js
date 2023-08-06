var tag = this;
tag.partners = opts.partners
tag.partner_class = opts.partner_class || "col-xs-12 no-padding";

this.on('mount', function() {
    tag.load_data(opts.data);
    tag.update();
});

load_data(data) {
    tag.participating_orgs = [];
    data.forEach(function(activity) {
	activity.participating_organisations.forEach(function(participating_org) {
	    if (participating_org.role.code == opts.participating_org_type
	        && tag.participating_orgs.map(function(s) { return s.organisation.code }).indexOf(participating_org.organisation.code) == -1) {
		tag.participating_orgs.push(participating_org);
	    }
	})
    });
    tag.participating_orgs.sort(function(o1, o2) { return o1.name > o2.name });
}
