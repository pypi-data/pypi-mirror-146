import logging
from functools import lru_cache
import warnings
from django.db.models import QuerySet
from django.contrib.gis import geos
from simple_locations.models import Area

logger = logging.getLogger(__name__)


@lru_cache()
def simplify_area(area_pk, simplify: float, dp: int):
    """
    simplify: simplify by decimal degrees
    At the equator, one degree = 111,139 m
    Therefore try simplifications of 1e5, 1e6, 1e7 etc
    dp: decimal points to include
    If not included, we'll try to pick an appropriate value from 'simplification'
    """
    area_type = None
    if not dp:
        dp = 1 / simplify

    def simplify_geom(geom):
        def _multipolygon(mp):
            return geos.MultiPolygon([_polygon(poly) for poly in mp])

        def _polygon(poly):
            lines = [_linearring(linear) for linear in poly]
            return geos.Polygon(*[single for single in lines if single])

        def _linearring(ls):
            ls = ls.clone()
            # Double transform here is probably a bit slow - however
            # it allows us to specify simplification tolerance in map units not
            # degrees
            simple = ls.simplify(tolerance=simplify)
            pts = [_point(pt) for pt in simple]
            if pts[0] != pts[-1]:
                pts.append(pts[0])
            # Drop points which are the same after simplify/truncate
            try:
                return geos.LinearRing(*pts)
            except Exception as E:
                warnings.warn(F'Unhandled legacy exception: {E}')
                pass

        def _point(pt):
            """ Drop decimal places from the point - we likely don't want such points in the output geoJSON """
            return (round(pt[0], dp), round(pt[1], dp))

        if isinstance(geom, geos.MultiPolygon):
            simplified_geom = _multipolygon(geom)
            area_type = "MultiPolygon"
        elif isinstance(geom, geos.Polgon):
            area_type = "Polygon"
            simplified_geom = _polygon(geom)
        else:
            raise NotImplementedError

        return area_type, simplified_geom

    geom = Area.objects.get(pk=area_pk).geom
    area_type, simplified_geom = simplify_geom(geom)

    return area_type, simplified_geom.coords


def as_geojson(areas: QuerySet, simplify: float, dp: int, properties: list = ['pk'], additional_properties: dict = None):

    def feature(area_pk):
        area_type, coords = simplify_area(area_pk, simplify=simplify, dp=dp)
        return {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "MultiPolygon", "coordinates": coords},
        }

    if 'pk' not in properties and 'id' not in properties:
        logger.warning('GeoJSON spec says you should include the primary key. Please add "pk" to list of properties.')
        properties.append('pk')

    # Prepare a dict of "properties" keyed off of PK
    # Common case is to want additional properties - for instance, 'dollars'
    # which may be provided as a dict
    properties = {p['pk']: p for p in areas.values(*properties)}
    if additional_properties:
        for pk, props in additional_properties.items():
            if pk in properties:
                properties[pk].update(**props)
    # Prepare features
    geojson = {"type": "FeatureCollection", "features": []}
    for area in areas:
        f = feature(area.pk)
        f['properties'] = properties[area.pk]
        geojson["features"].append(f)

    return geojson
