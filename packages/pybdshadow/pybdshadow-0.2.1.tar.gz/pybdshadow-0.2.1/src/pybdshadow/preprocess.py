"""
BSD 3-Clause License

Copyright (c) 2022, Qing Yu
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import shapely
import pandas as pd
import geopandas as gpd


def bd_preprocess(buildings, height='height'):
    '''
    Preprocess building data, so that we can perform shadow calculation.
    Remove empty polygons and convert multipolygons into polygons.

    **Parameters**
    buildings : GeoDataFrame
        Buildings.
    height : string
        Column name of building height

    **Return**
    allbds : GeoDataFrame
        Polygon buildings
    '''
    buildings = buildings[buildings.is_valid].copy()
    # 建筑高度筛选
    buildings[height] = pd.to_numeric(buildings[height], errors='coerce')
    buildings = buildings[-buildings[height].isnull()].copy()

    polygon_buildings = buildings[buildings['geometry'].apply(
        lambda r:type(r) == shapely.geometry.polygon.Polygon)]
    multipolygon_buildings = buildings[buildings['geometry'].apply(
        lambda r:type(r) == shapely.geometry.multipolygon.MultiPolygon)]
    allbds = []
    for j in range(len(multipolygon_buildings)):
        r = multipolygon_buildings.iloc[j]
        singlebd = gpd.GeoDataFrame()
        singlebd['geometry'] = list(r['geometry'].geoms)
        for i in r.index:
            if i != 'geometry':
                singlebd[i] = r[i]
        allbds.append(singlebd)
    allbds.append(polygon_buildings)
    allbds = pd.concat(allbds)
    allbds['building_id'] = range(len(allbds))
    return allbds
