/* exported QueryBuilder */

function QueryBuilder(data_url) {
    var self = this;
    var iso_date_pattern = /\d{4}-\d{1,2}-\d{1,2}/;
    // Riot provides our event emitter.
    riot.observable(self);


    function filter_hash(filters) {
        // returns a hash of the filter to key storage of previously calculated results
        return filters.reduce(function (hash, filter) { return hash + '?' + filter.name + ':' + filter.value; }, '');
    }

    // return a filtered set of transactions
    function set_filtered_objects(_filters) {
        // build the filters from the key values passed
        // multiple values in selects passed as multiple key value pairs with the same key
        var filters = _filters || [];
        var transactions = self.rich_transactions;
        var options = self.interface_options;
        var filtered_ids;
        var hash = filter_hash(filters);
        var transaction_id_arrays = {};
        var id_in_filter = {};

        function calculateActivityTransactionAmounts() {
            // Loop through the generated activities and create a "Transactions which Match" value
            var grouped_transactions = _.groupBy(self.filtered_transactions, 'activity_id');
            var group_by_values;
            _.each(grouped_transactions, function (transactionArray, activityId) {
                var activity = self.lookups.rich_activities_by_id[activityId];
                activity._filtered_transactions = transactionArray;
                activity._transaction_commitment = 0;
                activity._transaction_disbursement = 0;
                activity._transaction_expenditure = 0;
                activity._transaction_other = 0;
            });
            group_by_values = _.mapValues(grouped_transactions, function (o) { return _.groupBy(o, 'transaction_type_id'); });
            _.each(group_by_values, function (transaction_group, activity_id) {
                var activity = self.lookups.rich_activities_by_id[activity_id];
                _.each(transaction_group, function (_transactions, group_name) {
                    if (group_name === 'C') {
                        activity._transaction_commitment = _.sumBy(_transactions, 'usd_value');
                    } else if (group_name === 'D') {
                        activity._transaction_disbursement = _.sumBy(_transactions, 'usd_value');
                    } else if (group_name === 'E') {
                        activity._transaction_expenditure = _.sumBy(_transactions, 'usd_value');
                    } else {
                        activity._transaction_other += _.sumBy(_transactions, 'usd_value');
                    }
                });
            });
        }

        function setActivityFinanceTypes() {
            var to_display = function (d) {
                /* Pass me a dict of key=financetype, value=percent */
                var str = '';
                _.each(d, function (percentage, group) {
                    str += (group + ' (' + percentage + '%) ');
                });
                return str;
            };

            var to_percent_hash = function (groups) {
                var values_per_category = _.mapValues(groups, function (a) {
                    return _.sumBy(a, 'usd_value');
                });
                var total_value = _.sum(_.values(values_per_category));
                var values_per_category_percent = _.mapValues(values_per_category, function (v) {
                    return _.round((v / total_value) * 100);
                });
                return values_per_category_percent;
            };

            /* Add a 'percent financetype' to activities */
            /* First group by transaction */
            var commitments = _.filter(self.filtered_transactions, { transaction_type: 'Commitment' })
            var byActivity = _.groupBy(commitments, 'activity.id');
            /* Then group by finance type category */
            _.mapValues(byActivity, function (transaction_set, activityId) {
                var activity = self.lookups.rich_activities_by_id[activityId];
                var groups = _.groupBy(transaction_set, 'finance_category');
                if (_.keys(groups).length === 1) {
                    activity._financeCategoryTypes = _.keys(groups)[0];
                } else {
                    activity._financeCategoryTypes = to_display(to_percent_hash(groups));
                }
            });
        }

        // gets totals and statistics about a data set
        function data_set_stats() {
            var agg = _(_.mapValues(_.groupBy(self.filtered_transactions, 'transaction_type_id'), function (o) { return _.sumBy(o, 'usd_value'); }));

            self.filtered_stats = {
                total_commitment: agg.get('C'),
                total_disbursement: agg.get('D'),
                total_expenditure: agg.get('E'),
                total_other: agg.omit(['C', 'D', 'E']).values().sum()
            };
        }
        self.filter_cache = self.filter_cache || {};
        if (Object.prototype.hasOwnProperty.call(self.filter_cache, hash)) {
            filtered_ids = self.filter_cache[hash].filtered_ids;
        } else {
            _.each(filters, function (i) {
                var name = i.name;
                var value = i.value;

                if (name === 'start') {
                    if (!moment.isMoment(value)) { return; }
                    value = value.format('YYYY-MM-DD');
                    transaction_id_arrays[name] = _.map(_.filter(transactions, function (t) { return t.transaction_date >= value; }), 'id');
                    return;
                }
                if (name === 'end') {
                    if (!moment.isMoment(value)) { return; }
                    value = value.format('YYYY-MM-DD');
                    transaction_id_arrays[name] = _.map(_.filter(transactions, function (t) { return t.transaction_date <= value; }), 'id');
                    return;
                }

                if (Object.prototype.hasOwnProperty.call(transaction_id_arrays, name)) {
                    // combine id arrays with the same key with union
                    transaction_id_arrays[name] = _.union(transaction_id_arrays[name], options[name][value].transaction_ids);
                } else {
                    transaction_id_arrays[name] = options[name][value].transaction_ids;
                }
            });

            // combine id arrays of separate keys with intersection
            Object.keys(transaction_id_arrays).forEach(function (filter_name) {
                if (filtered_ids === undefined) {
                    filtered_ids = transaction_id_arrays[filter_name];
                } else {
                    filtered_ids = _.intersection(filtered_ids, transaction_id_arrays[filter_name]);
                }
            });
            self.filter_cache[hash] = { filtered_ids: filtered_ids };
        }

        // build quick lookup for efficient filtering
        if (filtered_ids !== undefined) {
            filtered_ids.forEach(function (id) { id_in_filter[id] = true; });
        }
        self.filtered_transactions = _.isUndefined(filtered_ids) ? transactions : transactions.filter(function (transaction) { return id_in_filter[transaction.id]; });
        self.filtered_activities = _(self.filtered_transactions).map('activity').uniqBy('id').value();
        calculateActivityTransactionAmounts();
        setActivityFinanceTypes();
        data_set_stats();
    }

    // get transactions aggregated by a given facet
    function apply_aggregation(transactions, aggregate_by) {
        var aggregated = {};
        var entries = [];
        var get_entries = self.aggregation_entry_functions[aggregate_by];
        var columns = ['commitment', 'disbursement', 'expenditure', 'other'];
        var titles;

        function aggregate_property_list(objects, key) {
            // Summarize a list of nested dicts to a single hash with all values in a list
            var r = {};
            var meta_columns = objects.map(key).map(_.keys).flatten().uniq();
            meta_columns.each(function (p) {
                r[p] = [];
                objects.each(function (o) {
                    if (!_.includes(r[p], o[key][p])) {
                        r[p].push(o[key][p]);
                    }
                });
            });
            return r;
        }

        // populate aggregate_entries with titles and totals from activities
        transactions.forEach(function (transaction) {
            try {
                entries = entries.concat(get_entries(transaction));
            } catch (err) {
                console.warn(err); // eslint-disable-line no-console
            }
        });

        // sum the values by unique titles
        titles = _(entries).map('title').uniq().value();
        _.map(titles, function (title) {
            var title_entries = _(entries).filter({ title: title });
            aggregated[title] = { title: title };
            _.map(columns, function (column) {
                aggregated[title][column] = title_entries.sumBy(column);
            });
            aggregated[title].meta = aggregate_property_list(title_entries, '_meta');
        });
        return _.values(aggregated);
    }

    function entry_from_transaction(transaction, title, multiplier, meta) {
        if (!multiplier) multiplier = 1;
        return {
            title: title,
            commitment: transaction.transaction_type_id === 'C' ? multiplier * transaction.usd_value : 0,
            disbursement: transaction.transaction_type_id === 'D' ? multiplier * transaction.usd_value : 0,
            expenditure: transaction.transaction_type_id === 'E' ? multiplier * transaction.usd_value : 0,
            other: /[^CDE]/.test(transaction.transaction_type_id) ? multiplier * transaction.usd_value : 0,
            _meta: meta || {}
        };
    }

    // return an entry for the organisation reporting the transaction
    function reporting_org_entry(transaction) {
        return entry_from_transaction(transaction, self.lookups.org_names[transaction.activity__reporting_organisation_id], undefined, { org_id: transaction.activity__reporting_organisation_id });
    }

    // return an entry for every sector a transaction is related to
    // TODO generalise, simplify etc...
    function sector_entries(transaction) {
        var entries = [];
        var pct_remaining = 1;
        var scale = 1;
        var total;
        var null_count;
        var i;

        // filter to only dac5s, and order by pct descending
        var activity_sectors = self.lookups.activity_sectors[transaction.activity_id];
        var dac5s = !activity_sectors ? [] : activity_sectors.filter(function (as) {
            return self.lookups.sector_dac3_names[as.sector_id] !== undefined;
        }).sort(function (a, b) {
            return b.pct - a.pct;
        });

        if (dac5s.length === 0) {
            // record activities with no sector dac5s
            entries.push(entry_from_transaction(transaction, 'No OECD DAC5 Sector'));
        } else {
            total = dac5s.reduce(function (t, d) { return t + (d.pct || 0); });
            null_count = dac5s.filter(function (d) { return !d; }).length;
            if (total < 100 && null_count === 0) {
                scale = total / 100;
            }

            Object.keys(dac5s).forEach(function (key) {
                var multiplier = pct_remaining;
                if (i < dac5s.length - 1) {
                    multiplier = scale * (dac5s[key].pct / 100) || (pct_remaining / (dac5s.length - i));
                }
                pct_remaining -= multiplier;
                entries.push(entry_from_transaction(transaction, self.lookups.sector_dac3_names[dac5s[key].sector_id], multiplier));
            });
        }

        return entries;
    }

    // return an entry for every national sector a transaction is related to
    function national_sector_entries(transaction) {
        var activity_national_sectors = self.lookups.activity_national_sectors[transaction.activity_id];
        var sectors = !activity_national_sectors ? [] : activity_national_sectors.filter(function (as) {
            return self.lookups.national_sectors[as.code] !== undefined;
        }).sort(function (a, b) {
            return b.percentage - a.percentage;
        });
        if (sectors.length === 0) { // record activities with no national sector
            return [entry_from_transaction(transaction, 'No National Sector')];
        };
        return _.map(sectors, function (sector) {
            // National Sector fields: activity : int = activity id, code: int = sector id, percentage, sector: str = sector name
            var title = self.lookups.national_sectors[sector.code]; /* return the name of an SWG / national sector */
            var entry = entry_from_transaction(transaction, title, sector.percentage / 100);
            return entry
        })
    }

    // return an entry for the organisation accountable for the activity
    function accountable_entries(transaction) {
        var all_orgs = self.lookups.activity_participating_organisations[transaction.activity_id];
        var orgs = all_orgs ? all_orgs.filter(function (apo) { return apo.role === 'Accountable'; }) : [];
        switch (orgs.length) {
            case 0:
                return entry_from_transaction(transaction, 'No Partner Ministry');
            case 1:
                return entry_from_transaction(transaction, self.lookups.org_names[orgs[0].organisation_id], undefined, { org_id: orgs[0].organisation_id });
            default:
                return entry_from_transaction(transaction, 'Multiple Partner Ministries');
        }
    }

    // constructs simple lookup objects from object arrays to bea enable efficient building of rich transaction and activity objects
    function build_lookup_objects(data) {
        var lookups;
        function code_name(data_set, field) { return _(data_set).keyBy('code').mapValues(field || 'name').value(); }
        function code_name_cap(data_set) {
            return _(data_set).keyBy('code').mapValues('name').mapValues(_.capitalize)
                .value();
        }
        function group(data_set) { return _.groupBy(data_set, 'activity_id'); }
        function org_name(org) { return _.upperFirst(_.trim(org.name, ' "\'')); }
        function dac_3_sector(sector) { return sector.code === sector.category__code; }

        lookups = {
            financial_year: data.transaction_fy_lookup,
            activity_info: _.keyBy(data.activities, 'id'),
            org_names: _(data.organisations).keyBy('code').mapValues(org_name).value(),
            org_abbreviations: _(data.organisations).keyBy('code').mapValues('abbreviation').value(),
            sector_dac3_names: code_name(_.filter(data.sectors, dac_3_sector)),
            finance_type_categories: {},
            activity_titles: {},

            /* Simple lookups take a "code" property and return a "name" or other slightly modified field */
            status_names: code_name(data.statuses),
            aid_type_names: code_name(data.aid_types),
            aid_type_categories: code_name(data.aid_type_categories),
            finance_type_names: code_name(data.finance_types),
            finance_type_category_ids: code_name(data.finance_types, 'category_id'),
            aid_type_category_ids: code_name(data.aid_types, 'category_id'),
            transaction_type_names: code_name(data.transaction_types),
            finance_type_category_names: code_name_cap(data.finance_type_categories),
            national_sectors: code_name(data.national_sectors),
            document_categories: code_name(data.document_categories),

            /* Build lookup hash tables grouped by "activity_id" */
            activity_locations: group(data.locations),
            activity_transactions: group(data.transactions),
            activity_participating_organisations: group(data.participating_organisations),
            activity_sectors: group(data.activity_sectors),
            activity_national_sectors: _.groupBy(data.national_sector_percentage, 'activity')
        };
        // build a finance type lookup table
        lookups.finance_type_categories = _(data.finance_types)
            .keyBy('code')
            .mapValues(function (c) { return lookups.finance_type_category_names[c.category_id]; })
            .value();

        // build a activity title lookup table
        lookups.activity_titles = _(data.titles)
            .groupBy('activity_id')
            .mapValues(function (t) { return (_.size(t) === 1 ? t[0] : _.find(t, { language: data.language || 'en' }) || t[0]).title; })
            .mapValues(function (t) { return _.upperFirst(_.trim(t, ' "\'')); })
            .value();

        return lookups;
    }

    // functions to support building rich objects

    // gets the financial year from a date string
    function get_financial_year(date_string) {
        var date;
        var y1;
        var y2;
        if (!iso_date_pattern.test(date_string)) { return [null, null]; }
        date = _.map(date_string.split('-'), _.toInteger);
        y1 = date[0];
        if (date[1] <= 2) y1 -= 1;
        y2 = y1 + 1;
        return [y1, 'FY ' + y1 + '/' + y2];
    }


    function build_rich_transaction(source_transaction) {
        var transaction = Object.create(source_transaction);
        var fy;

        transaction.provider = self.lookups.org_names[transaction.provider_organisation_id];
        transaction.receiver = self.lookups.org_names[transaction.receiver_organisation_id];
        transaction.aid_type = transaction.aid_type_id ? self.lookups.aid_type_names[transaction.aid_type_id] : self.lookups.aid_type_names[transaction.activity__default_aid_type_id];
        transaction.aid_type_category = self.lookups.aid_type_categories[self.lookups.aid_type_category_ids[transaction.aid_type_id || transaction.activity__default_aid_type_id]]
        transaction.finance_type_id = transaction.finance_type_id || transaction.activity__default_finance_type_id;
        transaction.finance_type = transaction.finance_type_id ? self.lookups.finance_type_names[transaction.finance_type_id] : 'None';
        transaction.finance_category_id = transaction.finance_type_id ? self.lookups.finance_type_category_ids[transaction.finance_type_id] : null;
        transaction.finance_category = transaction.finance_category_id ? self.lookups.finance_type_category_names[transaction.finance_category_id] : 'None';
        transaction.transaction_type = self.lookups.transaction_type_names[transaction.transaction_type_id];
        transaction.reporting_organisation_id = transaction.activity__reporting_organisation_id;
        transaction.reporting_organisation = self.lookups.org_names[transaction.reporting_organisation_id];
        transaction.activity_status_id = transaction.activity__activity_status_id;
        transaction.activity_status = self.lookups.status_names[transaction.activity__activity_status_id];
        transaction.completion = self.lookups.activity_info[transaction.activity_id].completion;
        fy = get_financial_year(transaction.transaction_date);
        transaction.financial_year_code = fy[0];
        transaction.financial_year = fy[1];

        return transaction;
    }

    function location_display(loc) {
        var name;
        if (loc.adm_country_adm1 === 'Nation-wide') name = 'Nationwide';
        else if (loc.adm_country_adm1 === 'Myanmar') name = 'Nationwide';
        else name = loc.name || loc.adm_country_adm2 + '(' + loc.adm_country_adm1 + ')';
        if (loc.percentage !== null) {
            return name + ' (' + loc.percentage + '%)';
        }
        return name;
    }

    function related_organisation_names(org_list) {
        return _.join(_.map(org_list, function (org) {
            return self.lookups.org_names[org.organisation_id];
        }), ', ');
    }

    function build_rich_activity(source_activity) {
        var activity = Object.create(source_activity);
        // Group activity organisations into "Funding", "Accountable", "Implementing" types
        activity.organisations = _.groupBy(self.lookups.activity_participating_organisations[activity.id], 'role');
        // Text to display in columns for different organisation classes related to the activity
        activity.funding_display = related_organisation_names(activity.organisations.Funding);
        activity.accountable_display = related_organisation_names(activity.organisations.Accountable);
        activity.implementing_display = related_organisation_names(activity.organisations.Implementing);
        activity.reporting = self.lookups.org_names[self.lookups.activity_info[activity.id].reporting_organisation_id];
        activity.status = self.lookups.status_names[self.lookups.activity_info[activity.id].activity_status_id];
        activity.commitment = 0;
        activity.disbursement = 0;
        activity.expenditure = 0;
        activity.other = 0;
        activity.title = self.lookups.activity_titles[activity.id];
        activity.locations = self.lookups.activity_locations[activity.id] || [];
        activity.location_display = activity.locations.length ? activity.locations.map(location_display).join(', ') : 'None';
        activity.transaction = self.lookups.activity_transactions[activity.id];
        return activity;
    }

    function extend_rich_activities() {
        /* Link transactions to activities and calculate financial totals  */
        var groupByTransactionType = function (o) { return _.groupBy(o, 'transaction_type_id'); };
        var grouped_transactions = _.groupBy(self.rich_transactions, 'activity_id');
        var group_by_values = _.mapValues(grouped_transactions, groupByTransactionType);
        var sumField = 'usd_value';
        var sumFunc = function (transactionArray) { return _.sumBy(transactionArray, sumField); };

        _.each(grouped_transactions, function (transactionArray, activity_id) { self.lookups.rich_activities_by_id[activity_id].transactions = transactionArray; });

        _.each(group_by_values, function (transactionGroups, activity_id) {
            var activity = self.lookups.rich_activities_by_id[activity_id];
            _.each(transactionGroups, function (transactionArray, transactionTypeCode) {
                if (transactionTypeCode === 'C') {
                    activity.commitment = sumFunc(transactionArray);
                } else if (transactionTypeCode === 'D') {
                    activity.disbursement = sumFunc(transactionArray);
                } else if (transactionTypeCode === 'E') {
                    activity.expenditure = sumFunc(transactionArray);
                } else {
                    activity.other += sumFunc(transactionArray);
                }
            });
        });
    }

    // Option Building

    // interates all transactions returning a number of option lists
    function build_interface_options() {
        var options = {
            reporting_organisations: {},
            accountable_organisations: {},
            funding_organisations: {},
            providing_organisations: {},
            sector_dac3s: {},
            national_sectors: {},
            finance_categories: {},
            transaction_types: {},
            activity_statuses: {},
            location_states: {},
            aid_types: {},
            aid_type_categories: {},
            document_categories: {},
        };

        // adds a new option if the option does not exist already
        // builds an array of transaction ids this option is a match for
        function add_or_increment_option(option_type, option_key, option_display, transaction_id) {
            if (!Object.prototype.hasOwnProperty.call(options[option_type], option_key)) {
                options[option_type][option_key] = { display: option_display, value: option_key, transaction_ids: [transaction_id] };
            } else {
                options[option_type][option_key].transaction_ids.push(transaction_id);
            }
        }

        self.rich_transactions.forEach(function (transaction) {
            function add_org_option(org_id, classed_as, option_display) {
                var option_type = classed_as + '_organisations';
                var option = option_display || self.lookups.org_names[org_id] + ' (' + self.lookups.org_abbreviations[org_id] + ')';
                add_or_increment_option(option_type, org_id, option, transaction.id);
            }

            // add transaction activity ID fields
            transaction.activity_iati_identifier = transaction.activity.iati_identifier;
            transaction.activity_internal_identifier = transaction.activity.internal_identifier;
            transaction.activity_id = transaction.activity.id;

            // add organisations to the filters
            add_org_option(transaction.reporting_organisation_id, 'reporting');
            _.each(transaction.activity.organisations.Accountable, function (org) {
                add_org_option(org.organisation_id, 'accountable');
            });
            if (_.size(transaction.activity.organisations.Accountable) === 0) {
                add_org_option('', 'accountable', 'No Accountable Organisation');
            }
            _.each(transaction.activity.organisations.Funding, function (org) {
                add_org_option(org.organisation_id, 'funding');
            });
            if (_.size(transaction.activity.organisations.Funding) === 0) {
                add_org_option('', 'funding', 'No Funding Organisation');
            }
            add_org_option(transaction.provider_organisation_id, 'providing');

            // OECD DAC3 sectors

            if (_.has(transaction, ['activity', 'sector_dac3s'])) {
                _.each(transaction.activity.sector_dac3s, function (sector) {
                    add_or_increment_option('sector_dac3s', sector.code, sector.sector, transaction.id);
                });
            } else {
                add_or_increment_option('sector_dac3s', '', 'No OECD (DAC3) sector', transaction.id);
            }

            if (_.has(transaction, ['activity', 'national_sectors'])) {
                _.each(transaction.activity.national_sectors, function (sector) {
                    add_or_increment_option('national_sectors', sector.code, sector.sector, transaction.id);
                });
            } else {
                add_or_increment_option('national_sectors', '', 'No National sector', transaction.id);
            }


            // finance category
            if (transaction.finance_category_id) {
                add_or_increment_option('finance_categories', transaction.finance_category_id, transaction.finance_category, transaction.id);
            } else {
                add_or_increment_option('finance_categories', '', 'No Finance Category', transaction.id);
            }

            // transaction types
            add_or_increment_option('transaction_types', transaction.transaction_type_id, transaction.transaction_type, transaction.id);

            // activity status
            add_or_increment_option('activity_statuses', transaction.activity_status_id, transaction.activity_status, transaction.id);

            // states
            if (transaction.activity.locations.length) {
                Object.keys(transaction.activity.locations).forEach(function (key) {
                    var loc = transaction.activity.locations[key];
                    add_or_increment_option('location_states', loc.adm_country_adm1, loc.adm_country_adm1, transaction.id);
                });
            } else {
                add_or_increment_option('location_states', '', 'No Location', transaction.id);
            }

            // aid types
            add_or_increment_option('aid_types', transaction.aid_type_id, transaction.aid_type, transaction.id);
            if (transaction.aid_type_category) {
                add_or_increment_option('aid_type_categories', transaction.aid_type__category_id, transaction.aid_type_category, transaction.id);
            }

            // document categories
            if (transaction.activity.document_categories.length) {
                _.each(transaction.activity.document_categories, function (cat) {
                    if (cat) {
                        add_or_increment_option('document_categories', cat, self.lookups.document_categories[cat], transaction.id);
                    } else {
                        add_or_increment_option('document_categories', '', 'No Documents', transaction.id);
                    }
                });
            } else {
                add_or_increment_option('document_categories', '', 'No Documents', transaction.id);
            }
        });
        self.interface_options = options;
    }

    // Interface Response

    // respond to requests for available filters and aggregations to fill form inputs
    self.on('request_available_filters', function () {
        RiotControl.trigger('available_filters', self.available_filters);
    });
    self.on('request_available_aggregations', function () {
        RiotControl.trigger('available_aggregations', self.available_aggregations);
    });

    // respond to requests for data
    self.on('request_filtered_activities', function () {
        RiotControl.trigger('filtered_activities', self.filtered_activities);
    });
    self.on('request_filtered_transactions', function () {
        RiotControl.trigger('filtered_transactions', self.filtered_transactions);
    });
    self.on('request_filtered_stats', function () {
        RiotControl.trigger('filtered_stats', self.filtered_stats);
    });
    self.on('request_filtered_aggregation', function () {
        RiotControl.trigger('filtered_aggregation', { selected: self.current_aggregation, data: self.filtered_aggregation });
    });

    // respond to requests to apply new filter
    self.on('apply_filter', function on_apply_filter(filter) {
        set_filtered_objects(filter);
        self.filtered_aggregation = apply_aggregation(self.filtered_transactions, self.current_aggregation.id);

        RiotControl.trigger('filtered_activities', self.filtered_activities);
        RiotControl.trigger('filtered_transactions', self.filtered_transactions);
        RiotControl.trigger('filtered_stats', self.filtered_stats);
        RiotControl.trigger('filtered_aggregation', { selected: self.current_aggregation, data: self.filtered_aggregation });
    });
    self.on('apply_aggregation', function on_aggregate_by(aggregate_by) {
        self.current_aggregation = aggregate_by;
        self.filtered_aggregation = apply_aggregation(self.filtered_transactions, self.current_aggregation.id);
        RiotControl.trigger('filtered_aggregation', { selected: self.current_aggregation, data: self.filtered_aggregation });
    });

    // initialize call to data api
    self.on('fetch', function(){
        $.get(data_url).then(function (data) {
            var rich_activities_by_id = {};

            // build some lookup objects for performance
            var lookups = build_lookup_objects(data);
            self.lookups = lookups;

            // build rich objects for fast filtering
            self.rich_activities = data.activities.map(build_rich_activity);

            // build activity id lookup
            rich_activities_by_id = _.keyBy(self.rich_activities, 'id');
            self.lookups.rich_activities_by_id = rich_activities_by_id;

            // Rich activity - dac3 sectors

            function dac3_display(list) {
                if (_.size(list) === 0) { return 'None'; }
                return _.join(_.map(list, function (s) { return s.percentage === 100 ? s.sector : s.sector + '(' + s.percentage + '%)'; }), ',');
            }
            /* Attach sector category info and a display property to each Activity */
            _.each(data.activity_sector_categories, function (activity_sectors, activity_code) {
                if (!_.has(rich_activities_by_id, activity_code)) { return; }
                _.each(activity_sectors, function (sector) { sector.sector = data.sector_categories[sector.code]; });
                rich_activities_by_id[activity_code].sector_dac3s = activity_sectors;
                rich_activities_by_id[activity_code].sector_dac3_display = dac3_display(activity_sectors);
            });

            _.each(_.groupBy(data.national_sector_percentage, 'activity'), function (activity_sectors, activity_code) {
                if (!_.has(rich_activities_by_id, activity_code)) { return; }
                _.each(activity_sectors, function (sector) {
                    sector.code = sector.sector;
                    sector.sector = lookups.national_sectors[sector.sector];
                });
                rich_activities_by_id[activity_code].national_sectors = activity_sectors;
                rich_activities_by_id[activity_code].national_sectors_display = dac3_display(activity_sectors);
            });

            self.rich_transactions = data.transactions.map(build_rich_transaction);
            // build transaction activity links
            _.each(self.rich_transactions, function (t) { t.activity = rich_activities_by_id[t.activity_id]; });

            // extend rich activities with information gleaned from transactions
            extend_rich_activities();

            // Build all possible options for interface filters
            build_interface_options();


            // filters available to be used by the interface
            self.available_filters = [
                { id: 'reporting_organisations', name: 'Reporting Organisation', options: self.interface_options.reporting_organisations },
                { id: 'accountable_organisations', name: 'Partner Ministry', options: self.interface_options.accountable_organisations },
                { id: 'funding_organisations', name: 'Funding Organisation', options: self.interface_options.funding_organisations },
                { id: 'providing_organisations', name: 'Providing Organisation', options: self.interface_options.providing_organisations },
                { id: 'sector_dac3s', name: 'OECD (DAC3) Sector', options: self.interface_options.sector_dac3s },
                { id: 'national_sectors', name: 'National Sector', options: self.interface_options.national_sectors },
                { id: 'finance_categories', name: 'Finance Category', options: self.interface_options.finance_categories },
                { id: 'transaction_types', name: 'Transaction Type', options: self.interface_options.transaction_types },
                { id: 'activity_statuses', name: 'Activity Status', options: self.interface_options.activity_statuses },
                { id: 'location_states', name: 'Location', options: self.interface_options.location_states },
                { id: 'aid_types', name: 'Aid Type', options: self.interface_options.aid_types },
                { id: 'aid_type_categories', name: 'Aid Type Category', options: self.interface_options.aid_type_categories },
                { id: 'document_categories', name: 'Document Category', options: self.interface_options.document_categories }
            ];


            // aggregations available to be used by the interface
            self.available_aggregations = [
                { id: 'reporting_organisation', name: 'Reporting Organisation' },
                { id: 'accountable_organisation', name: 'Partner Ministry' },
                { id: 'providing_organisation', name: 'Providing Organisation' },
                { id: 'sector_dac3', name: 'OECD Sector (DAC3)' },
                { id: 'national_sectors', name: 'National Sector' },
                { id: 'aid_type_categories', name: 'Aid Type Categories' },
                { id: 'finance_categories', name: 'Finance Type Categories' },
            ];

            // functions to retrieve aggregation entries
            self.aggregation_entry_functions = {
                reporting_organisation: reporting_org_entry,
                sector_dac3: sector_entries,
                national_sectors: national_sector_entries,
                providing_organisation: function (transaction) { return entry_from_transaction(transaction, transaction.provider, undefined, { org_id: transaction.provider }); },
                accountable_organisation: accountable_entries,
                aid_type_categories: function (transaction) { return entry_from_transaction(transaction, transaction.aid_type_category); },
                finance_categories: function(transaction){return entry_from_transaction(transaction, transaction.finance_category);  },
            };

            // perform initial filter
            set_filtered_objects([{ name: 'start', value: window.openly_filters.start_date }, { name: 'end', value: window.openly_filters.end_date }]);
            self.current_aggregation = self.available_aggregations[0];
            self.filtered_aggregation = apply_aggregation(self.filtered_transactions, self.current_aggregation.id);

            self.all_aggregations = function () {
                return _.map(self.available_aggregations, function (agg) { return { data: apply_aggregation(self.filtered_transactions, agg.id), name: agg.name }; });
            };
        }).then(function(){
            RiotControl.trigger('hide_loader');
            RiotControl.trigger('available_filters', self.available_filters);
            RiotControl.trigger('available_aggregations', self.available_aggregations);
            RiotControl.trigger('filtered_activities', self.filtered_activities);
            RiotControl.trigger('filtered_transactions', self.filtered_transactions);
            RiotControl.trigger('filtered_stats', self.filtered_stats);
            RiotControl.trigger('filtered_aggregation', { selected: self.current_aggregation, data: self.filtered_aggregation });
        });
    })
}
