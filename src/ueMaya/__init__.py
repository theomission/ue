import os

import maya.cmds
import maya.OpenMayaUI
import sip

import ueSpec

import ueCore.AssetUtils as ueAssetUtils

from PyQt4 import QtCore

def getMayaWindow():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

# Parses the fileInfo from a list to a dict
def parseFileInfo(fi):
    fiDict = {}
    for i in range(len(fi)/2):
        fiDict[fi[i*2]] = fi[i*2+1]
    return fiDict

def ueNewScriptSetup():
    spec = ueSpec.Spec(os.getenv("PROJ"),
                       os.getenv("GRP"),
                       os.getenv("ASST"))

    asset = ueAssetUtils.getAsset(spec)

    # Set up renderer - default to Mental Ray
    maya.cmds.loadPlugin("Mayatomr.so")
    maya.cmds.setAttr("defaultRenderGlobals.currentRenderer", "mentalRay", type="string")

    # Set up the timeline
    maya.cmds.playbackOptions(animationStartTime=float(asset["startFrame"]),
                              animationEndTime=float(asset["endFrame"]),
                              minTime=float(asset["startFrame"]),
                              maxTime=float(asset["endFrame"]))

    x = int(asset["xRes"])+int(asset["xPad"])
    y = int(asset["yRes"])+int(asset["yPad"])

    # Set up renderGlobals
    maya.cmds.setAttr("defaultRenderGlobals.outFormatControl", 0)
    maya.cmds.setAttr("defaultRenderGlobals.animation", 1)
    maya.cmds.setAttr("defaultRenderGlobals.startFrame", float(asset["startFrame"]))
    maya.cmds.setAttr("defaultRenderGlobals.endFrame", float(asset["endFrame"]))
    maya.cmds.setAttr("defaultResolution.pixelAspect", float(asset["aspectRatio"]))
    maya.cmds.setAttr("defaultResolution.deviceAspectRatio", float(x)/float(y))
    maya.cmds.setAttr("defaultResolution.width", x)
    maya.cmds.setAttr("defaultResolution.height", y)

    # Render file name
    #maya.cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
    #maya.cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)

