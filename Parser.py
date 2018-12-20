from xml.sax import make_parser, handler
# from pymongo import MongoClient
# from pprint import pprint
import simplejson as json


class OSMNode:
    def __init__(self, attrs=[]):
        self.id = attrs["id"]
        self.lat = attrs["lat"]
        self.lon = attrs["lon"]
        self.tags = []

    def addTag(self, tag):
        self.tags.append(tag)

class OSMRelation:
    def __init__(self, attrs=[]):
        self.id = attrs["id"]
        self.tags = []
        self.members = []

    def addMember(self,member):
        self.members.append(member)

    def addTag(self, tag):
        self.tags.append(tag)

class OSMWay:
    def __init__(self, attrs):
        self.id = attrs["id"]
        self.nds = []
        self.tags = []

    def addNd(self, nd):
        self.nds.append(nd)

    def addTag(self, tag):
        self.tags.append(tag)


class OSMTag:
    def __init__(self, attrs=[]):
        self.k = attrs["k"]
        self.v = attrs["v"]

class OSMNd:
    def __init__(self, attrs=[]):
        self.ref = attrs["ref"]

class OSMMember:
    def __init__(self, attrs=[]):
        self.type = attrs["type"]
        self.ref = attrs["ref"]

class OSMSax(handler.ContentHandler):
    def __init__(self, db):
        self.db = db

    def startElement(self, name, attrs):
        if (name == "node"):
            self.currentElement = OSMNode(attrs)
        if (name == "way"):
            self.currentElement = OSMWay(attrs)
        if (name == "relation"):
            self.currentElement = OSMRelation(attrs)
        if (name == "tag"):
            tag = OSMTag(attrs)
            self.currentElement.addTag(tag)
        if (name == "nd"):
            nd = OSMNd(attrs)
            self.currentElement.addNd(nd)
        if (name == "member"):
            member = OSMMember(attrs)
            self.currentElement.addMember(member)

    def endElement(self, name):
        if (name == "node"):
            jnode = json.dumps(self.currentElement, default=lambda x: x.__dict__)
            print(jnode)
        if (name == "way"):
            jway = json.dumps(self.currentElement, default=lambda x: x.__dict__)
            print(jway)
        if (name == "relation"):
            jrelation = json.dumps(self.currentElement, default=lambda x: x.__dict__)
            print(jrelation)



db = "temp"
# client = MongoClient(port=27017)
# db = client.OSM.OSM_Node
# db.drop()


parser = make_parser()
b = OSMSax(db)
parser.setContentHandler(b)
parser.parse("C:\\Users\\marvi\Desktop\\Programmieren\\Unity\\Project World\\deutz_small.osm")
