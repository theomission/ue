import sys, json
import httplib, urllib

import ueSpec

global client

# Recursively url encode a multidimensional dictionary by
# pablobm via stackoverflow. Thank you!
# http://stackoverflow.com/questions/4013838/urlencode-a-multidimensional-dictionary-in-python
def recursive_urlencode(d):
    def recursion(d, base=None):
        pairs = []

        for key, value in d.items():
            if hasattr(value, 'values'):
                pairs += recursion(value, key)
            else:
                new_pair = None
                if base:
                    new_pair = "%s[%s]=%s" % (base, urllib.quote(unicode(key)), urllib.quote(unicode(value)))
                else:
                    new_pair = "%s=%s" % (urllib.quote(unicode(key)), urllib.quote(unicode(value)))
                pairs.append(new_pair)
        return pairs

    return '&'.join(recursion(d))

class Client():
    def __init__(self):
        global client

        self.protocol = "http"
        self.name = "localhost"
        self.port = 3000
        self.host = "%s:%i" % (self.name, self.port)
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "text/plain"}

        client = self

    def get(self, get, *args):
        if get == "assets":
            get = "ueassets"

        urlargs = self.parseUrlargs(args)

        url = "/%s%s.json" % (get, urlargs)

        try:
            con = httplib.HTTPConnection(self.host)
            con.request("GET", url)
            request = con.getresponse()
        except IOError, e:
            print "FATAL ERROR: %s" % e
            sys.exit(2)

        try:
            jsonDict = json.load(request)
        except ValueError:
            jsonDict = {}

        if jsonDict == None:
            jsonDict = {}

        return jsonDict

    def post(self, post, *args, **kwargs):
        if post == "assets":
            post = "ueassets"

        urlargs = self.parseUrlargs(args)

        url = "/%s%s.json" % (post, urlargs)

        try:
            con = httplib.HTTPConnection(self.host)
            con.request("POST", url, recursive_urlencode(kwargs["data"]), self.headers)
            request = con.getresponse()
        except IOError, e:
            print "FATAL ERROR: %s" % e
            sys.exit(2)

    def put(self, put, *args, **kwargs):
        if put == "assets":
            put = "ueassets"

        urlargs = self.parseUrlargs(args)

        url = "/%s%s.json" % (put, urlargs)

        try:
            con = httplib.HTTPConnection(self.host)
            con.request("PUT", url, recursive_urlencode(kwargs["data"]), self.headers)
            request = con.getresponse()
        except IOError, e:
            print "FATAL ERROR: %s" % e
            sys.exit(2)

    def destroy(self, delete, *args):
        if delete == "assets":
            delete = "ueassets"

        urlargs = self.parseUrlargs(args)

        url = "/%s%s.json" % (delete, urlargs)

        try:
            con = httplib.HTTPConnection(self.host)
            con.request("DELETE", url)
            request = con.getresponse()
        except IOError, e:
            print "FATAL ERROR: %s" % e
            sys.exit(2)


    def parseUrlargs(self, args):
        if len(args) > 0:
            urlargs = "/"+str("/".join(args))
        else:
            urlargs = ""
        return urlargs


    def getProjects(self):
        return self.get("projects")

    def getProject(self, spec):
        return self.get("projects", spec.proj)

    def getGroups(self, spec):
        return self.get("groups", spec.proj)

    def getGroup(self, spec):
        return self.get("groups", spec.proj, spec.grp)

    def getAssets(self, spec):
        return self.get("assets", spec.proj, spec.grp)

    def getAsset(self, spec):
        return self.get("assets", spec.proj, spec.grp, spec.asst)

    def getElements(self, spec):
        return self.get("elements", spec.proj, spec.grp, spec.asst)

    def getElement(self, spec):
        return self.get("elements", spec.proj, spec.grp, spec.asst,
                        spec.elclass, spec.eltype, spec.elname)


    def saveProject(self, spec, data):
        self.post("projects", data={"project": data})

    def saveGroup(self, spec, data):
        self.post("groups", spec.proj, data={"group": data})

    def saveAsset(self, spec, data):
        self.post("assets", spec.proj, spec.grp,
                  data={"asset": data})

    def saveElement(self, spec, data):
        self.post("elements", spec.proj, spec.grp, spec.asst,
                  spec.elclass, spec.eltype, spec.elname,
                  data={"element": data})

    def saveVersion(self, spec, data):
        self.post("versions", spec.proj, spec.grp, spec.asst,
                  spec.elclass, spec.eltype, spec.elname,
                  data={"version": data})


    def updateProject(self, spec, data):
        self.put("projects", spec.proj, data={"project": data})

    def updateGroup(self, spec,  data):
        self.put("groups", spec.proj, spec.grp, data={"group": data})

    def updateAsset(self, spec, data):
        self.put("ueassets", spec.proj, spec.grp, spec.asst,
                  data={"asset": data})

    def updateElement(self, spec, data):
        self.put("elements", spec.proj, spec.grp, spec.asst,
                 spec.elclass, spec.eltype, spec.elname,
                 data={"element": data})

    def updateVersion(self, spec, data):
        self.put("versions", spec.proj, spec.grp, spec.asst,
                 spec.elclass, spec.eltype, spec.elname,
                 data={"version": data})


    def destroyProject(self, spec):
        self.destroy("projects", spec.proj)

    def destroyGroup(self, spec):
        self.destroy("groups", spec.proj, spec.grp)

    def destroyAsset(self, spec):
        self.destroy("assets", spec.proj, spec.grp, spec.asst)

    def destroyElement(self, spec):
        self.destroy("elements", spec.proj, spec.grp, spec.asst,
                  spec.elclass, spec.eltype, spec.elname)

    def destroyVersion(self, spec):
        self.destroy("versions", spec.proj, spec.grp, spec.asst,
                  spec.elclass, spec.eltype, spec.elname, str(spec.vers))

