function DonorProvider() {
    riot.observable(this);

    var self = this;
    self.requests = {};

    self.one('request_stats', function(){
        // console.log('requesting commitments by category ' + djangoUrls['commitment_by_category']);
        self.requests['commitment_by_category'] = $.get(djangoUrls['commitment_by_category'])
            .done(function(data) {
                self.trigger('commitment_by_category', data);
            }).fail(function(data){
                console.error('fail commitment_by_category');
            }).always(function(){
                delete self.requests['commitment_by_category'];
            });
    });

    self.one('request_activities_status_values', function(){
        // console.log('requesting activity status values' + djangoUrls['activities_status_values']);
        self.requests['activities_status_values'] = $.get(djangoUrls['activities_status_values'])
            .done(function(data) {
                self.trigger('activities_status_values', data);
            }).fail(function(data){
                console.error('fail activities_status_values');
            }).always(function(){
                delete self.requests['activities_status_values'];
            });
    });

    self.one('request_transactions_by_year', function(){
        // console.log('requesting transaction values' + djangoUrls['transactions_by_year']);
        self.requests['transactions_by_year'] = $.get(djangoUrls['transactions_by_year'])
            .done(function(data) {
                self.trigger('transactions_by_year', data);
            }).fail(function(data){
                console.error('fail transactions_by_year');
            }).always(function(){
                delete self.requests['transactions_by_year'];
            });
    });

    self.one('request_activities', function(){
        // console.log('requesting activities values' + djangoUrls['activities']);
        self.requests['activities'] = $.get(djangoUrls['activities'])
            .done(function(data) {
                self.trigger('activities', data);
            }).fail(function(data){
                console.error('fail activities');
            }).always(function(){
                delete self.requests['activities'];
            });
    });
}
