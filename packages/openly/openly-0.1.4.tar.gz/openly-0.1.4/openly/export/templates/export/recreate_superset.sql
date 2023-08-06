-- For consistent formatting please do
-- python3 -m sqlparse -r -s ./supersetify.sql -o ./supersetify.sql
-- Note that much of this is auto generated to align with Excel and CSV formats
-- This file should be accessible at http://localhost:8000/en/export/supersetsecretsquirrel/

-- This is a workaround for "SimpleLocations" not being on mohinga yet
-- This does essentially what 'Location.objects.sync_simple()' does
UPDATE aims_location SET area_id = (SELECT id FROM simple_locations_area WHERE simple_locations_area.code = aims_location.adm_code);

DROP SCHEMA IF EXISTS superset CASCADE;
CREATE SCHEMA IF NOT EXISTS superset;
{% for class in models %} {% if class.raw_sql %}
CREATE TABLE superset.{{ class.cache_properties.module|lower }} AS {{ class.raw_sql|safe }};
{% endif %}{% endfor %}