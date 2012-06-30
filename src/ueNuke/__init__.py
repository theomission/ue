import os, sys, glob

import nuke, nukescripts

import ueSpec

import ueCore.AssetUtils as ueAssetUtils

checks = {
 "Framerate": {
          "FPS":         {
                          "name": "FPS",
                          "check": "float(nuke.root().knob(\"fps\").value()) != float(os.getenv(\"FRAME_RATE\"))",
                          "update": "nuke.root().knob(\"fps\").setValue(float(os.getenv(\"FRAME_RATE\")))",
                          "curval": "float(nuke.root().knob(\"fps\").value())",
                          "newval": "float(os.getenv(\"FRAME_RATE\"))"
                         },
          "Start Frame": {
                          "name": "Start frame",
                          "check": "float(nuke.root().knob(\"first_frame\").value()) != float(os.getenv(\"FIRST_FRAME\"))",
                          "update": "nuke.root().knob(\"first_frame\").setValue(float(os.getenv(\"FIRST_FRAME\")))",
                          "curval": "float(nuke.root().knob(\"first_frame\").value())",
                          "newval": "float(os.getenv(\"FIRST_FRAME\"))"
                         },
          "End Frame":   {
                          "name": "End frame",
                          "check": "float(nuke.root().knob(\"last_frame\").value()) != float(os.getenv(\"LAST_FRAME\"))",
                          "update": "nuke.root().knob(\"last_frame\").setValue(float(os.getenv(\"LAST_FRAME\")))",
                          "curval": "float(nuke.root().knob(\"last_frame\").value())",
                          "newval": "float(os.getenv(\"LAST_FRAME\"))"
                         }
         },
 "Asset": {
          "Project":     {
                          "name": "Project",
                          "check": "nuke.root().knob(\"ueproj\").value() != os.getenv(\"PROJ\")",
                          "update": "nuke.root().knob(\"ueproj\").setValue(os.getenv(\"PROJ\"))",
                          "curval": "nuke.root().knob(\"ueproj\").value()",
                          "newval": "os.getenv(\"PROJ\")"
                         },
          "Group":       {
                          "name": "Group",
                          "check": "nuke.root().knob(\"uegrp\").value() != os.getenv(\"GRP\")",
                          "update": "nuke.root().knob(\"uegrp\").setValue(os.getenv(\"GRP\"))",
                          "curval": "nuke.root().knob(\"uegrp\").value()",
                          "newval": "os.getenv(\"GRP\")"
                         },
          "Asset":       {
                          "name": "Asset",
                          "check": "nuke.root().knob(\"ueasst\").value() != os.getenv(\"ASST\")",
                          "update": "nuke.root().knob(\"ueasst\").setValue(os.getenv(\"ASST\"))",
                          "curval": "nuke.root().knob(\"ueasst\").value()",
                          "newval": "os.getenv(\"ASST\")"
                         }
        }
}

def ueNewScriptSetup():
    root = nuke.root()

    context = ueSpec.Context()
    spec = context.spec

    asset = ueAssetUtils.getAsset(spec)

    formatName = "ueProjectRes"

    root.knob("fps").setValue(int(asset["frameRate"]))
    root.knob("first_frame").setValue(int(asset["startFrame"]))
    root.knob("last_frame").setValue(int(asset["endFrame"]))

    x = int(asset["xRes"])+int(asset["xPad"])
    y = int(asset["yRes"])+int(asset["yPad"])

    nuke.addFormat("%i %i %s" % (x, y, formatName))
#    nuke.addFormat("%i %i %i %i %i %i %d %s" % (x, y, int(config["xPad"]), int(config["yPad"]),
#                                                int(config["xRes"]), int(config["yRes"]),
#                                                float(config["aspectRatio"]), formatName))
    root.knob("format").setValue(formatName)

    os.environ["FRAME_RATE"] = asset["frameRate"]
    os.environ["FIRST_FRAME"] = asset["startFrame"]
    os.environ["LAST_FRAME"] = asset["endFrame"]

def ueReadAsset(node, cmd=None, name=None):
    n = nuke.createNode(node)

    if name is not None:
        n.setName(name)

    if cmd == None:
        cmd = node

    n.addKnob(nuke.PyScript_Knob("ueOpen"+cmd, "     Browse Elements     ",
                                 "import ueNuke.Open\nueNuke.Open.ueOpen"+cmd+"()"))

    n.addKnob(nuke.String_Knob("proj", "project"))
    n.addKnob(nuke.String_Knob("grp", "group"))
    n.addKnob(nuke.String_Knob("asst", "asset"))
    n.addKnob(nuke.String_Knob("elclass", "class"))
    n.addKnob(nuke.String_Knob("eltype", "type"))
    n.addKnob(nuke.String_Knob("elname", "name"))
    n.addKnob(nuke.Int_Knob("vers", "version"))
    n.addKnob(nuke.String_Knob("elpass", "pass"))

    n.knob("file").setValue("[python get"+cmd+"Path()]")
    n.knob("label").setValue("[value proj]:[value grp]:[value asst]\n"+\
                             "[value elname]:[value eltype]:[value elclass] v[value vers]")

    return n

def ueWriteAsset(node, cmd=None, name=None):
    n = nuke.createNode(node)

    if name is not None:
        n.setName(name)

    if cmd == None:
        cmd = node

    n.addKnob(nuke.PyScript_Knob("ueOpen"+cmd, "     Browse Elements     ",
                                 "import ueNuke.Save\nueNuke.Save.ueSave"+cmd+"()"))

    n.addKnob(nuke.String_Knob("proj", "project"))
    n.addKnob(nuke.String_Knob("grp", "group"))
    n.addKnob(nuke.String_Knob("asst", "asset"))
    n.addKnob(nuke.String_Knob("elclass", "class"))
    n.addKnob(nuke.String_Knob("eltype", "type"))
    n.addKnob(nuke.String_Knob("elname", "name"))
#    n.addKnob(nuke.String_Knob("elpass", "pass"))

    n.knob("file").setValue("/tmp/temp.%04d.exr")
    n.knob("label").setValue("[value proj]:[value grp]:[value asst]\n"+\
                             "[value elname]:[value eltype]:[value elclass]")

    return n

def getReadPath():
#    n = nuke.thisParent()
    n = nuke.thisNode()

    elpass = n.knob("elpass").value()
    if elpass == "":
        elpass = None

    spec = ueSpec.Spec(n.knob("proj").value(),
                       n.knob("grp").value(),
                       n.knob("asst").value(),
                       n.knob("elclass").value(),
                       n.knob("eltype").value(),
                       n.knob("elname").value(),
                       n.knob("vers").value(),
                       elpass)

    p = os.path.join(os.getenv("UE_PATH"), "lib",
                     "placeholders", "nuke.png")

    if not spec.proj == "" and not spec.grp == "" and \
       not spec.asst == "" and not spec.elclass == "" and \
       not spec.eltype == "" and not spec.elname == "" and \
       not spec.vers == "":
        versions = ueAssetUtils.getVersions(spec)
        if int(spec.vers) > len(versions):
            return p
        v = versions[int(spec.vers)-1]
        if not v == {}:
            elpassDir = ""
            elpassFile = ""
            if not spec.elpass == None:
                elpassDir = spec.elpass
                elpassFile = "_"+spec.elpass
            files = glob.glob(os.path.join(v["path"], elpassDir,
                                           v["file_name"]+elpassFile+"*"))
            if len(files) > 0:
                ext = files[0].split(".")[-1]

                if len(files) == 1:
                    p = os.path.join(v["path"], elpassDir,
                                     v["file_name"]+elpassFile+"."+ext)
                else:
                    p = os.path.join(v["path"], elpassDir,
                                     v["file_name"]+elpassFile+".%04d."+ext)

                nuke.thisNode().knob("first").setValue(1)
                nuke.thisNode().knob("last").setValue(len(files))
                nuke.thisNode().knob("origfirst").setValue(1)
                nuke.thisNode().knob("origlast").setValue(len(files))

    return p

def getReadGeoPath():
#    n = nuke.thisParent()
    n = nuke.thisNode()

    spec = ueSpec.Spec(n.knob("proj").value(),
                       n.knob("grp").value(),
                       n.knob("asst").value(),
                       n.knob("elclass").value(),
                       n.knob("eltype").value(),
                       n.knob("elname").value(),
                       n.knob("vers").value())

    p = os.path.join(os.getenv("UE_PATH"), "lib",
                     "placeholders", "nuke.obj")

    if not spec.proj == "" and not spec.grp == "" and \
       not spec.asst == "" and not spec.elclass == "" and \
       not spec.eltype == "" and not spec.elname == "" and \
       not spec.vers == "":
        versions = ueAssetUtils.getVersions(spec)
        if int(spec.vers) > len(versions):
            return p
        v = versions[int(spec.vers)-1]
        if not v == {}:
            files = glob.glob(os.path.join(v["path"], v["file_name"]+"*.obj"))
            if len(files) < 1:
                return p
            ext = files[0].split(".")[-1]
            if len(files) == 1:
                p = os.path.join(v["path"], v["file_name"]+"."+ext)
            else:
                p = os.path.join(v["path"], v["file_name"]+".%04d."+ext)
#                p = os.path.join(v["path"], elpassDir,
#                                 v["file_name"]+elpassFile+".%04d."+ext)

    return p

