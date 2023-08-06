from django.utils.translation import gettext_lazy as _

# Sector types to distinguish iati (DAC) sectors from local host country sectors
OPENLY_SECTOR_TYPE_IATI = "iati"
OPENLY_SECTOR_TYPE_NATIONAL = "national"

OPENLY_SECTOR_TYPES = (
    (OPENLY_SECTOR_TYPE_IATI, _("Iati Codelist Sector")),
    (OPENLY_SECTOR_TYPE_NATIONAL, _("National Sector")),
)
