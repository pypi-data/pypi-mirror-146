from django.utils.translation import gettext_lazy as _


non_iati_sector_object = _('Coordination Body')
non_iati_sector_object_report = _('Coordination Body Report')
non_iati_sector_title = _('Coordination Bodies')
non_iati_sector_text = _('Coordination Bodies are multi-stakeholder dialogue bodies responsible for ensuring that development priorities are identified, discussed and implemented in a co-ordinated and transparent manner.')

# Shepherd bits
shepherd_welcome_header = _('Welcome to Mohinga')
shepherd_welcome_aims = _('Mohinga is Myanmar\'s Aid Information Management System (AIMS).')
shepherd_welcome_partners = _('The Mohinga application allows development partners to report their assistance to Myanmar in a simple, common, comparable format.')

shepherd_welcome_disclaimer = _('Disclaimer')
shepherd_welcome_disclaimer_partners = _('Data contained within Mohinga has been collected in partnership with Myanmar’s development partners as part of an ongoing process of collaboration and dialogue.')
shepherd_welcome_disclaimer_contactfirst = _('Before using the data, we encourage all users to first contact the relevant development partners to ensure data is accurate.')

shepherd_search_header = _('Search within Mohinga')
shepherd_search_finding = _('Mohinga contains a lot of information. To find what you’re looking for try searching by development partner, activity or sector')
shepherd_search_profilepages = _('Profile pages')
shepherd_search_profilepages_page = _('Each development partner also has a dedicated profile page with information on all their activities')
shepherd_search_profilepages_access = _('You can access their profile pages by searching for their name here')

shepherd_visualise_header = _('Visualise aid flows')
shepherd_visualise_dashboards = _('Mohinga visualises aid flows to Myanmar via four interactive dashboards')
shepherd_visualise_by = _('you can see aid by location, donor, sector or Ministry responsible')
shepherd_visualise_link = _('Click here to access the dashboards')

shepherd_filtering_header = _('Filtering the dashboard by date')
shepherd_filtering_date = _('The date filter allows you to filter information presented on the dashboards between a specific time period')
shepherd_filtering_select = _('Select a start and end date and then click the refresh button to set the filter')

shepherd_export_header = _('Exporting data from Mohinga')
shepherd_export_download = _('The export function will download the dashboard data to a .CSV file')
shepherd_export_selecting = _('Also, if you have set a date range or zoomed into Shan state or selected a specific organisation, clicking export will just give you that data')

shepherd_activity_header = _('Activity List')
shepherd_activity_calculation = _('Data from all of the activities below is used to calculate the figures that appear in the dashboard above.')
shepherd_activity_page = _('Click on the blue activity number in the Activity List to visit the Activity Profile page and learn more.')

shepherd_complete = _('That is it... for now')
shepherd_complete_further = _('If you need any further information')
shepherd_complete_help_icons = _('look for these help icons')
shepherd_complete_help_icons_further = _('and they will provide you with some additional information about Mohinga.')
shepherd_complete_working_hard = _('We are also working hard to bring new features and functions to Mohinga')
shepherd_complete_info = _(
    'These include advanced reporting tools and better integration with internationally available IATI aid data ' +
    'as well as other tools to help make the management of aid information simple, time efficient and even enjoyable. ' +
    'We will be in touch.')

# What to call "Non government" on the partners page
partner_page_NGOs = 'UN & Multilateral'

# Hamutuk wants "activities" to be called "programs"
activity_or_program = _('Activity')
activities_or_programs = _('Activities')
# TODO: Move this to Hamutuk
simple_locations_text = _('Locations represent where the %(activity_or_program)s takes place. For %(activities_or_programs)s in Manufahi, add all relevant aldeias. For %(activities_or_programs)s in other municipalities, add all relevant sub-districts. To select a location please type your location in the search bar.' % {'activity_or_program': activity_or_program.lower(), 'activities_or_programs': activities_or_programs.lower()})

contact_edit_job_title = _('Please input clearly a title of job')
contact_edit_phone = _('Input phone number for this contact')
contact_edit_name = _('Input name of person for this contact')
