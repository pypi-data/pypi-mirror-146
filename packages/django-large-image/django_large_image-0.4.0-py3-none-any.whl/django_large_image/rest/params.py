from drf_yasg import openapi

projection = openapi.Parameter(
    'projection',
    openapi.IN_QUERY,
    description='The projection in which to open the image (try `EPSG:3857`).',
    type=openapi.TYPE_STRING,
)

z = openapi.Parameter('z', openapi.IN_PATH, description='zoom level', type=openapi.TYPE_INTEGER)
x = openapi.Parameter('x', openapi.IN_PATH, description='x', type=openapi.TYPE_INTEGER)
y = openapi.Parameter('y', openapi.IN_PATH, description='y', type=openapi.TYPE_INTEGER)

# Style Parameters
palette = openapi.Parameter(
    'palette',
    openapi.IN_QUERY,
    description='The color palette to map the band values (named Matplotlib colormaps or palettable palettes).',
    type=openapi.TYPE_STRING,
)
band = openapi.Parameter(
    'band',
    openapi.IN_QUERY,
    description='The band number to use.',
    type=openapi.TYPE_INTEGER,
)
vmin = openapi.Parameter(
    'min',
    openapi.IN_QUERY,
    description='The minimum value for the color mapping.',
    type=openapi.TYPE_NUMBER,
)
vmax = openapi.Parameter(
    'max',
    openapi.IN_QUERY,
    description='The maximum value for the color mapping.',
    type=openapi.TYPE_NUMBER,
)
nodata = openapi.Parameter(
    'nodata',
    openapi.IN_QUERY,
    description='The value to map as no data (often made transparent).',
    type=openapi.TYPE_NUMBER,
)
scheme = openapi.Parameter(
    'scheme',
    openapi.IN_QUERY,
    description='This is either ``linear`` (the default) or ``discrete``. If a palette is specified, ``linear`` uses a piecewise linear interpolation, and ``discrete`` uses exact colors from the palette with the range of the data mapped into the specified number of colors (e.g., a palette with two colors will split exactly halfway between the min and max values).',
    type=openapi.TYPE_STRING,
)

STYLE = [palette, band, vmin, vmax, nodata, scheme]

# Region Parameters
left = openapi.Parameter(
    'left', openapi.IN_QUERY, description='left', type=openapi.TYPE_NUMBER, required=True
)
right = openapi.Parameter(
    'right', openapi.IN_QUERY, description='right', type=openapi.TYPE_NUMBER, required=True
)
top = openapi.Parameter(
    'top', openapi.IN_QUERY, description='top', type=openapi.TYPE_NUMBER, required=True
)
bottom = openapi.Parameter(
    'bottom', openapi.IN_QUERY, description='bottom', type=openapi.TYPE_NUMBER, required=True
)
units = openapi.Parameter(
    'units',
    openapi.IN_QUERY,
    description='The projection/units of the region coordinates.',
    type=openapi.TYPE_STRING,
)

REGION = [left, right, top, bottom, units]

# Histogram Parameters
only = openapi.Parameter(
    'onlyMinMax',
    openapi.IN_QUERY,
    type=openapi.TYPE_BOOLEAN,
    default=False,
)
bins = openapi.Parameter(
    'bins',
    openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    default=256,
)
density = openapi.Parameter(
    'density',
    openapi.IN_QUERY,
    type=openapi.TYPE_BOOLEAN,
    default=False,
)
format = openapi.Parameter(
    'format',
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
)

HISTOGRAM = [only, bins, density, format]
