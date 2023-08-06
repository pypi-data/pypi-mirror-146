{% load i18n %}

var self = this

self.loading = true;
self.first_statistics_year = ''
self.total_commitments = 0;
self.total_disbursements = 0;
self.percentage_dibursements_executed = ''
self.num_activities = ''
self.commitment_by_category = ''

// mount event is fired when tag is ready in the DOM - wrtie jquery and data requests here
self.on('mount', function(){
    RiotControl.trigger('request_stats')
    $("#statistics").popover({placement:'right'});
    $("#sectors").popover({placement:'right'});
})

// commitment_by_category event fired by ajax component - listen to it here and update diaplyed data
RiotControl.on('commitment_by_category', function(data){
    self.commitment_by_category = data
    self.update();
})

// activities event fired by ajax component - listen to it here and update diaplyed data
RiotControl.on('activities', function(data){
    self.num_activities = data.activities.length

    self.update();
})

RiotControl.on('transactions_by_year', function(data){
    for( var i=0;i< data.length;i++){
        self.total_commitments += Number(data[i].Commitments);
        self.total_disbursements = Number(data[i].Disbursements);
        if(data[i].year){
            var year = data[i].year
            if( self.first_statistics_year == '' || year < self.first_statistics_year ){
                self.first_statistics_year = year
            }
        }
    }
    self.loading = false;
    self.update();
})
