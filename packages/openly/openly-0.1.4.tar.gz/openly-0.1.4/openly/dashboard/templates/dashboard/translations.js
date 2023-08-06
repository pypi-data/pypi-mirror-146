{% load i18n %}

var dashboard_translations = {
    filter_helps: {
        reporting_organisations: "{% trans "The organisation responsible for the accuracy, completeness, and timeliness of the information about this activity. The reporting organisation is not necessarily involved in the activity itself, though in practice it often will be a development partner providing funding." %}",
        accountable_organisations: "{% trans "The Government entity or entities with whom the activity has been agreed." %}",
        funding_organisations: "{% trans "The government or organisation which provides funds to the activity." %}",
        providing_organisations: "{% trans "The organisation providing the money for the transaction." %}",
        sector_dac3s: "{% trans "The specific areas of the recipient’s economic or social development that the transfer intends to foster. The sector labels and codes used are tertiary-level OECD-DAC sector codes." %}",
        national_sectors: "{% trans "National Sectors" %}",
        finance_categories: "{% trans "DAC/CRS transaction classification used to distinguish financial instruments, e.g. grants or loans." %}",
        transaction_types: "{% trans "Transactions recording committed or actual funds flowing in or out of an aid activity (e.g. commitment, disbursement, expenditure, etc.)." %}",
        activity_status: "{% trans "Lifecycle status of the activity from pipeline to completion." %}",
        financial_years: "{% trans "Myanmar's fiscal year runs from 1 April to 31 March." %}",
        location_states: "{% trans "Myanmar is divided into 7 divisions, 7 states, 1 Union Territory." %}",
        document_categories: "{% trans "Documents associated with an Activity have a given category." %}"
    }
};
