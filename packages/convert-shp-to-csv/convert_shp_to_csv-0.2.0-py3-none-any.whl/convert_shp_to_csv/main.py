# Ignore warnings around version mismatch that doesn't affect results
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

import argparse
import os.path
import geopandas as gpd
import shapely
import numpy as np
from haversine import inverse_haversine, Direction


def main():
    description = """
Converts a shape file (.shp) to a gridded csv file.
    """

    arg_parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    arg_parser.add_argument("shape_file", type=str, help="Shape file (.shp) to convert")
    arg_parser.add_argument(
        "--output-file", "-o", type=str, help="Name of csv file to output", default=None
    )
    arg_parser.add_argument(
        "--cell-size",
        type=float,
        help="Cell size, in kilometers. Default: 10",
        default=10.0,
    )

    # Parse arguments and
    args = arg_parser.parse_args()
    shape_file_name = os.path.basename(args.shape_file)
    if args.output_file is None:
        output_csv_name = f"{os.path.splitext(shape_file_name)[0]}.csv"
    else:
        output_csv_name = args.output_file

    # Convert a shape file to a geodataframe
    shp = gpd.read_file(args.shape_file)

    # Pull list of data columns we want to include in the output
    # Basically, anything that is not the `geometry`
    # TODO: Allow specification of desired columns via cli arguments?
    columns = [col for col in shp.columns if col != "geometry"]

    # Determine geometric values
    xmin, ymin, xmax, ymax = shp.total_bounds

    # Build list of boxes representing the grid that covers the full shape image rectangle
    grid_cells = []
    x, y = xmin, ymin
    while y < ymax:
        next_y = inverse_haversine((x, y), args.cell_size, Direction.EAST)[1]
        while x < xmax:
            next_x = inverse_haversine((x, y), args.cell_size, Direction.NORTH)[0]
            grid_cells.append(
                shapely.geometry.box(x, y, next_x, next_y)
            )
            x = next_x
        x = xmin
        y = next_y

    # Create a GeoDataFrame based on the grid cells, setting a value that represents the center of the cell
    gridded = gpd.GeoDataFrame(geometry=grid_cells)
    gridded["centroid"] = gridded.geometry.apply(lambda x: x.centroid)

    gridded.set_crs(shp.crs, inplace=True)

    # Join the shape file with the grid by overlaying the shape over the grid and then removing cells whose centers
    # are outside the defined shape(s).
    gdf = gpd.sjoin(
        gridded,
        shp,
    )

    # Convert the grid location to latitude and longitude
    gdf["latitude"] = gdf.centroid.apply(lambda x: x.y)
    gdf["longitude"] = gdf.centroid.apply(lambda x: x.x)

    # Pull out only the lat/long columns + the data columns from the shape file determined above
    df = gdf[["latitude", "longitude"] + columns]

    # Save the dataframe as a CSV
    df.to_csv(output_csv_name, index=False)


if __name__ == "__main__":
    main()
