import itertools
import logging.config
import math
import re
import socket
import time
import warnings
from itertools import chain
from typing import List, Union

import networkx as nx
import numpy as np
import overpy
import pyproj
from heapdict import heapdict
from overpy import Result
from tqdm.auto import tqdm

from pyridy.osm.utils import QueryResult, OSMLevelCrossing, OSMRailwaySwitch, OSMRailwaySignal, OSMRailwayLine, \
    OSMRailwayElement, OSMRailwayMilestone, calc_angle_between
from pyridy.utils.tools import internet

logger = logging.getLogger(__name__)


class OSM:
    supported_railway_types = ["rail", "tram", "subway", "light_rail"]

    def __init__(self, lon_sw: float, lat_sw: float, lon_ne: float, lat_ne: float,
                 desired_railway_types: Union[List, str] = None, download: bool = True, recurse: str = ">"):

        if None in [lon_sw, lat_sw, lon_ne, lat_ne]:
            raise ValueError("One or more lat/lon values is None")

        if desired_railway_types is None:
            desired_railway_types = ["rail", "tram", "subway", "light_rail"]
        else:
            if type(desired_railway_types) == list:
                for desired in desired_railway_types:
                    if desired not in OSM.supported_railway_types:
                        raise ValueError("Your desired railway type %s is not supported" % desired)
            elif type(desired_railway_types) == str:
                if desired_railway_types not in OSM.supported_railway_types:
                    raise ValueError("Your desired railway type %s is not supported" % desired_railway_types)
            else:
                raise ValueError("desired_railway_types must be list or str")

        if lon_sw == lon_ne or lat_sw == lat_ne:
            raise ValueError("Invalid coordinates")

        if not (-90 <= lat_sw <= 90) or not (-90 <= lat_ne <= 90):
            raise ValueError("Lat. value outside valid range")

        if not (-180 <= lon_sw <= 180) or not (-180 <= lon_ne <= 180):
            raise ValueError("Lon. value outside valid range")

        self.overpass_api = overpy.Overpass()
        self.overpass_api_alt = overpy.Overpass(url="https://overpass.kumi.systems/api/interpreter")
        self.overpass_api_ifs = overpy.Overpass(url="http://134.130.76.80:12345/api/interpreter")

        self.lon_sw = lon_sw
        self.lat_sw = lat_sw
        self.lon_ne = lon_ne
        self.lat_ne = lat_ne

        self.utm_proj = pyproj.Proj(proj='utm', zone=32, ellps='WGS84', preserve_units=True)
        self.geod = pyproj.Geod(ellps='WGS84')

        self.desired_railway_types = desired_railway_types

        self.nodes: List[overpy.Node, overpy.RelationNode] = []
        self.node_dict = {}

        self.ways: List[overpy.Way, overpy.RelationWay] = []
        self.way_dict = {}

        self.railway_lines: List[OSMRailwayLine] = []
        self.railway_elements: List[OSMRailwayElement] = []

        self.query_results = {rw_type: {"track_query": QueryResult,
                                        "route_query": QueryResult} for rw_type in self.desired_railway_types}

        self.G = nx.MultiGraph()

        if download:
            self.download_track_data(recurse=recurse)

            # Add nodes to Graph
            self.G.add_nodes_from([(n.id, n.__dict__) for n in self.nodes])

            # Add edges, use node distances as weight
            for w in self.ways:
                edges = [(n1.id, n2.id, self.geod.inv(float(n1.lon), float(n1.lat), float(n2.lon), float(n2.lat))[2])
                         for n1, n2 in zip(w.nodes, w.nodes[1:])]
                self.G.add_weighted_edges_from(edges, weight="d", way_id=w.id)

            if len(self.G.nodes) > 0:
                self._check_allowed_switch_transits()
            else:
                logger.warning("Can't check allowed switch transits, because the Graph has no nodes!")

        logger.info("Initialized region: %f, %f (SW), %f, %f (NE)" % (self.lon_sw,
                                                                      self.lat_sw,
                                                                      self.lon_ne,
                                                                      self.lat_ne))

    def _create_query(self, railway_type: str, recurse: str = ">"):
        if recurse not in [">", ">>", "<", "<<"]:
            raise ValueError("recurse type %s not supported" % recurse)

        if railway_type not in OSM.supported_railway_types:
            raise ValueError("The desired railway type %s is not supported" % railway_type)

        track_query = """(node[""" + "railway" + """=""" + railway_type + """](""" + str(self.lat_sw) + """,""" + str(
            self.lon_sw) + """,""" + str(self.lat_ne) + """,""" + str(self.lon_ne) + """);
                         way[""" + "railway" + """=""" + railway_type + """](""" + str(self.lat_sw) + """,""" + str(
            self.lon_sw) + """,""" + str(self.lat_ne) + """,""" + str(self.lon_ne) + """););
                         (._;>;);
                         out body;
                      """
        if railway_type == "rail":  # Railway routes use train instead of rail
            railway_type = "train"

        route_query = """(relation[""" + "route" + """=""" + railway_type + """](""" + str(self.lat_sw) + """,""" \
                      + str(self.lon_sw) + """,""" + str(self.lat_ne) + """,""" + str(self.lon_ne) + """);
                        );
                        (._;""" + recurse + """;);
                         out body;
                      """

        return track_query, route_query

    def _check_allowed_switch_transits(self):
        """ Checks in what ways a switch can be transited, i.e. what combination of neighbouring nodes are allowed

        """
        if not len(self.G.nodes):
            raise ValueError("Can't determine allowed switch transits if Graph G has no nodes")

        for sw in self.get_switches():
            sw_x, sw_y = self.utm_proj(sw.lon, sw.lat)
            sw_nbs = list(self.G.adj[sw.id])

            allowed_transits = []
            for n1, n2 in itertools.product(sw_nbs, repeat=2):
                if n1 == n2:
                    continue
                else:
                    n1_x, n1_y = self.G.nodes[n1]['attributes'].get('x', 0), self.G.nodes[n1]['attributes'].get('y', 0)
                    n2_x, n2_y = self.G.nodes[n2]['attributes'].get('x', 0), self.G.nodes[n2]['attributes'].get('y', 0)

                    v1 = [n1_x - sw_x, n1_y - sw_y]
                    v2 = [n2_x - sw_x, n2_y - sw_y]

                    ang = calc_angle_between(v1, v2)
                    if ang > math.pi / 2:
                        allowed_transits.append((n1, sw.id, n2))

            sw.allowed_transits = allowed_transits
            self.G.nodes[sw.id]['attributes']['allowed_transits'] = allowed_transits
        pass

    def download_track_data(self, railway_type: Union[List, str] = None, recurse: str = ">"):
        if recurse not in [">", ">>", "<", "<<"]:
            raise ValueError("recurse type %s not supported" % recurse)

        if railway_type:
            railway_types = [railway_type]
        else:
            railway_types = self.desired_railway_types

        # Download data for all desired railway types
        if internet():
            for railway_type in tqdm(railway_types):
                # Create Overpass queries and try downloading them
                logger.info("Querying data for railway type: %s" % railway_type)
                trk_query, rou_query = self._create_query(railway_type=railway_type, recurse=recurse)
                trk_result = QueryResult(self.query_overpass(trk_query), railway_type)
                rou_result = QueryResult(self.query_overpass(rou_query), railway_type)
                self.query_results[railway_type]["track_query"] = trk_result
                self.query_results[railway_type]["route_query"] = rou_result

                # Convert relation result to OSMRailwayLine objects
                if rou_result.result:
                    for rel in rou_result.result.relations:
                        rel_way_ids = [mem.ref for mem in rel.members if
                                       type(mem) == overpy.RelationWay and not mem.role]

                        if trk_result.result:
                            rel_ways = [w for w in trk_result.result.ways if w.id in rel_way_ids]

                            sort_order = {w_id: idx for w_id, idx in zip(rel_way_ids, range(len(rel_way_ids)))}
                            rel_ways.sort(key=lambda w: sort_order[w.id])
                            self.railway_lines.append(OSMRailwayLine(rel.id, rel_ways, rel.tags, rel.members))

                if trk_result.result:
                    for n in trk_result.result.nodes:
                        if n not in self.nodes:
                            self.nodes.append(n)

                        if "railway" in n.tags:
                            if n.tags["railway"] == "level_crossing":
                                self.railway_elements.append(OSMLevelCrossing(n))
                            elif n.tags["railway"] == "signal":
                                self.railway_elements.append(OSMRailwaySignal(n))
                            elif n.tags["railway"] == "switch":
                                self.railway_elements.append(OSMRailwaySwitch(n))
                            elif n.tags["railway"] == "milestone":
                                self.railway_elements.append(OSMRailwayMilestone(n))
                            else:
                                pass

                    for w in trk_result.result.ways:
                        if w not in self.ways:
                            self.ways.append(w)

                    # Create dictionaries for easy node/way access
                    self.node_dict = {n.id: n for n in self.nodes}  # Dict that returns node based on node id
                    self.way_dict = {w.id: w for w in self.ways}  # Dict that returns way based on way id

                    # Add XY coordinate to each node
                    osm_xy = self.get_coords(frmt="xy")
                    for i, xy in enumerate(osm_xy):
                        self.nodes[i].attributes["x"] = xy[0]
                        self.nodes[i].attributes["y"] = xy[1]
        else:
            logger.warning("Cant download OSM data because of not internet connection")

    def query_overpass(self, query: str, attempts: int = 3) -> Result:
        if internet(host="134.130.76.80", port=12345):  # IFS internal Overpass instance
            for a in range(attempts):
                time.sleep(a)
                try:
                    logger.info("Trying to query OSM data, %d/%d tries" % (a, attempts))
                    result = self.overpass_api_ifs.query(query)
                    logger.info("Successfully queried OSM Data using IFS Overpass instance")
                    return result
                except overpy.exception.OverpassTooManyRequests as e:
                    logger.warning("OverpassTooManyRequest, retrying".format(e))
                except overpy.exception.OverpassRuntimeError as e:
                    logger.warning("OverpassRuntimeError, retrying".format(e))
                except overpy.exception.OverpassGatewayTimeout as e:
                    logger.warning("OverpassTooManyRequest, retrying".format(e))
                except overpy.exception.OverpassBadRequest as e:
                    logger.warning("OverpassTooManyRequest, retrying".format(e))
                except socket.timeout as e:
                    logger.warning("Socket timeout, retrying".format(e))

        for a in range(attempts):  # Default Overpass instance
            time.sleep(a)
            try:
                logger.info("Trying to query OSM data, %d/%d tries" % (a, attempts))
                result = self.overpass_api.query(query)
                logger.info("Successfully queried OSM Data using default Overpass instance")
                return result
            except overpy.exception.OverpassTooManyRequests as e:
                logger.warning("OverpassTooManyRequest, retrying".format(e))
            except overpy.exception.OverpassRuntimeError as e:
                logger.warning("OverpassRuntimeError, retrying".format(e))
            except overpy.exception.OverpassGatewayTimeout as e:
                logger.warning("OverpassTooManyRequest, retrying".format(e))
            except overpy.exception.OverpassBadRequest as e:
                logger.warning("OverpassTooManyRequest, retrying".format(e))
            except socket.timeout as e:
                logger.warning("Socket timeout, retrying".format(e))

        logger.info("Using alternative Overpass API url")
        for a in range(attempts):
            time.sleep(a)
            try:
                logger.info("Trying to query OSM data, %d/%d tries" % (a, attempts))
                result = self.overpass_api_alt.query(query)
                logger.info("Successfully queried OSM Data using alternative IFS instance")
                return result
            except overpy.exception.OverpassTooManyRequests as e:
                logger.warning("OverpassTooManyRequest, retrying".format(e))
            except overpy.exception.OverpassRuntimeError as e:
                logger.warning("OverpassRuntimeError, retrying".format(e))
            except overpy.exception.OverpassGatewayTimeout as e:
                logger.warning("OverpassTooManyRequest, retrying".format(e))
            except overpy.exception.OverpassBadRequest as e:
                logger.warning("OverpassTooManyRequest, retrying".format(e))
            except socket.timeout as e:
                logger.warning("Socket timeout, retrying".format(e))
        else:
            logger.warning("Could download OSM data via Overpass after %d attempts with query: %s" % (attempts,
                                                                                                      query))
            return None

    def get_all_route_nodes(self) -> list:
        """ Retrieves a list of nodes part of any relation/route

        Returns
        -------
        List[overpy.node]
        """
        nodes = []

        for railway_type in self.desired_railway_types:
            nodes.append(self.query_results[railway_type]["route_query"].result.nodes)

        return list(chain.from_iterable(nodes))

    def get_shortest_path(self, source: int, target: int, weight: str, method="dijkstra") -> List[int]:
        """ Calculates the shortest path between a source and target node. Also considers how switches can be transited
        Based on: https://en.wikipedia.org/wiki/Dijkstra

        Parameters
        ----------
        source: int
            ID of source node
        target: int
            ID of target node
        weight: str
            Weight to be used for shortest path calculation, e.g. the length of the edges
        method: str
            Can be 'dijkstra' or 'A*'

        Returns
        -------
        List[int]
            List of node ids that represent the shortest path between source and target
        """
        dist = {n: np.inf for n in self.G.nodes}
        prev = {n: None for n in self.G.nodes}

        if method == "dijkstra":
            dist[source] = 0

            Q = heapdict()
            for v in self.G.nodes:
                Q[v] = dist[v]

            while Q:
                u = Q.popitem()[0]

                if u == target:
                    break

                u_is_switch = True if self.G.nodes[u]['tags'].get('railway') == 'switch' else False

                for v in set(self.G.adj[u]).intersection(set(Q.keys())):  # Neighbors of u that are still in Q
                    if u_is_switch:
                        u_prev = prev[u]
                        allowed = True if (u_prev, u, v) in self.G.nodes[u]['attributes'].get('allowed_transits',
                                                                                              []) else False
                    else:
                        allowed = True

                    alt = dist[u] + self.G[u][v][0][weight]
                    if allowed and alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
                        Q[v] = alt

        elif method == 'A*':
            s_lon, s_lat = float(self.G.nodes[source]['lon']), float(self.G.nodes[source]['lat'])
            t_lon, t_lat = float(self.G.nodes[target]['lon']), float(self.G.nodes[target]['lat'])

            dist[source] = 0 + self.geod.inv(s_lon, s_lat, t_lon, t_lat)[2]

            Q = heapdict()
            for v in self.G.nodes:
                Q[v] = dist[v]

            while Q:
                u = Q.popitem()[0]

                if u == target:
                    break

                u_is_switch = True if self.G.nodes[u]['tags'].get('railway') == 'switch' else False

                for v in set(self.G.adj[u]).intersection(set(Q.keys())):  # Neighbors of u that are still in Q
                    v_lon, v_lat = float(self.G.nodes[v]['lon']), float(self.G.nodes[v]['lat'])

                    if u_is_switch:
                        u_prev = prev[u]
                        allowed = True if (u_prev, u, v) in self.G.nodes[u]['attributes'].get('allowed_transits',
                                                                                              []) else False
                    else:
                        allowed = True

                    alt = dist[u] + self.G[u][v][0][weight] + self.geod.inv(v_lon, v_lat, t_lon, t_lat)[2]
                    if allowed and alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
                        Q[v] = alt
        else:
            raise ValueError("Method not supported")

        S = []  # Shortest path sequence
        u = target

        if prev[u] or u == source:
            while u:
                S.append(u)
                u = prev[u]

        S.reverse()

        return dist, prev, S

    def search_osm_result(self, way_ids: List[int], railway_type="tram"):
        ways = []

        for way_id in way_ids:
            for way in self.query_results[railway_type].result.ways:
                if way_id == way.id:
                    ways.append(way)

        return ways

    def get_coords(self, frmt: str = "lon/lat") -> np.ndarray:
        """ Get the coordinates in lon/lat format for all nodes

        Parameters
        ----------
            frmt: str, default: lon/lat
                Format in which the coordinates are being returned. Can be lon/lat or x/y

        Returns
        -------
            np.ndarray
        """
        if frmt not in ["lon/lat", "xy"]:
            raise ValueError("fmrt must be lon/lat or xy")

        if self.nodes:
            if frmt == "lon/lat":
                return np.array([[float(n.lon), float(n.lat)] for n in self.nodes])
            else:
                lat_lon_coords = np.array([[float(n.lon), float(n.lat)] for n in self.nodes])
                x, y = self.utm_proj(lat_lon_coords[:, 0], lat_lon_coords[:, 1])
                return np.vstack([x, y]).T
        else:
            logger.warning("No nodes get coordinates of!")
            return np.array([])

    def get_switches(self) -> List[OSMRailwayElement]:
        """ Returns a list of railway switches found in the downloaded OSM region

        Returns
        -------
            list
        """
        return [el for el in self.railway_elements if type(el) == OSMRailwaySwitch]

    def get_switches_for_railway_line(self, line: OSMRailwayLine) -> List[OSMRailwaySwitch]:
        """ Get switches part of a given railway line

        Parameters
        ----------
        line: OSMRailwayLine

        Returns
        -------
            list
        """
        switches = self.get_switches()

        line_switches = []
        for w in line.ways:
            n_ids = [n.id for n in w.nodes]
            for sw in switches:
                if sw.id in n_ids:
                    line_switches.append(sw)

        return line_switches

    def get_signals(self) -> List[OSMRailwayElement]:
        """ Returns a list of railway signals found in the downloaded OSM region

        Returns
        -------
            list
        """
        return [el for el in self.railway_elements if type(el) == OSMRailwaySignal]

    def get_milestones(self) -> List[OSMRailwayElement]:
        """ Returns a list of railway milestones found in the downloaded OSM region

        Returns
        -------
            list
        """
        return [el for el in self.railway_elements if type(el) == OSMRailwayMilestone]

    def get_level_crossings(self) -> List[OSMRailwayElement]:
        """ Returns a list of railway level crossings found in the downloaded OSM region

        Returns
        -------
            list
        """
        return [el for el in self.railway_elements if type(el) == OSMLevelCrossing]

    def get_railway_line(self, name) -> [OSMRailwayLine]:
        """ Get railway line by name. Always returns a list, even if only one line is found that matches the name

        Parameters
        ----------
        name: str
            Name of the railway line that should be searched

        Returns
        -------
            list
        """
        return [line for line in self.railway_lines if re.search(r'\b{0}\b'.format(name), line.name)]

    @property
    def lon_sw(self):
        return self._lon_sw

    @lon_sw.setter
    def lon_sw(self, value: float):
        if -180 <= value <= 180:
            self._lon_sw = value
        else:
            warnings.warn("You are trying to set non plausible longitude value %f, keeping existing value"
                          % self.lon_sw, UserWarning)

    @property
    def lat_sw(self):
        return self._lat_sw

    @lat_sw.setter
    def lat_sw(self, value: float):
        if -90 <= value <= 90:
            self._lat_sw = value
        else:
            warnings.warn("You are trying to set non plausible latitude value %f, keeping existing value"
                          % self.lat_sw, UserWarning)

    @property
    def lon_ne(self):
        return self._lon_ne

    @lon_ne.setter
    def lon_ne(self, value: float):
        if -180 <= value <= 180:
            self._lon_ne = value
        else:
            warnings.warn("You are trying to set non plausible longitude value %f, keeping existing value"
                          % self.lon_ne, UserWarning)

    @property
    def lat_ne(self):
        return self._lat_ne

    @lat_ne.setter
    def lat_ne(self, value: float):
        if -90 <= value <= 90:
            self._lat_ne = value
        else:
            warnings.warn("You are trying to set non plausible latitude value %f, keeping existing value"
                          % self.lat_ne, UserWarning)

    def __repr__(self):
        return "Lat SW: %f, Lon SW: %f , Lat NE: %f, Lon NE: %f" % (self.lat_sw,
                                                                    self.lon_sw,
                                                                    self.lat_ne,
                                                                    self.lon_ne)
