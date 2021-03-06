import os, glob

import ueNuke
import ueNuke.Save as ueNukeSave
import ueNuke.Open as ueNukeOpen
import ueNuke.Read as ueNukeRead
import ueNuke.Render as ueNukeRender
import ueNuke.Load as ueNukeLoad

import ueCommon.Checker as ueCommonChecker
import ueCommon.Save as ueCommonSave
import ueCommon.Open as ueCommonOpen
import ueCommon.Render as ueCommonRender

# Utilities
def ueRead():
    p = nuke.getPaneFor("Properties.1")
    ueReadPanel.addToPane(p)

def ueChecker(show=False):
    # The following two lines are a bit of a hack to make sure the
    # script checker gets updated every time its opened.
    # Else, when you open a new script, the panel doesn't get redrawn
    # and it 'saves' the info from then previous script.
    # Un-registering and regstering the widget seems to do the trick.
    nukescripts.unregisterPanel("ue.panel.ueChecker", None)
    ueCheckerPanel = nukescripts.registerWidgetAsPanel("ueCommonChecker.Checker",
                                                       "ueChecker", "ue.panel.ueChecker",
                                                       create=True)
    if show:
        ueCheckerPanel.show()
    else:
        p = nuke.getPaneFor("Properties.1")
        ueCheckerPanel.addToPane(p)

def nukeChecker():
    for group in ueNuke.checks:
        for check in ueNuke.checks[group]:
            c = ueNuke.checks[group][check]
            if c["type"] == "single":
                if (lambda: eval(c["check"]))():
                    ueChecker(show=True)
                    break

# Tool bar menus
ueMenu = "ue&Tools"
# File utils
nuke.menu("Nuke").addCommand(ueMenu+"/&Open",
                             ueNukeOpen.ueOpen, "Ctrl+o")
nuke.menu("Nuke").addCommand(ueMenu+"/&Save",
                             ueNukeSave.ueSave, "Ctrl+s")
nuke.menu("Nuke").addCommand(ueMenu+"/Save &As...",
                             ueNukeSave.ueSaveAs, "Ctrl+Shift+s")
nuke.menu("Nuke").addCommand(ueMenu+"/Save New &Version",
                             ueNukeSave.ueSaveVers, "Ctrl+Alt+s")
nuke.menu("Nuke").addCommand(ueMenu+"/-", "")
# Gizmo menu
ueNukeLoad.addGizmos()
# Nodes menu
nuke.menu("Nuke").addCommand(ueMenu+"/nodes/ueRead", "ueReadAsset(\"Read\")")
nuke.menu("Nuke").addCommand(ueMenu+"/nodes/ueReadGeo", "ueReadAsset(\"ReadGeo\", cmd=\"ReadGeo\")")
nuke.menu("Nuke").addCommand(ueMenu+"/nodes/ueAtomReadGeo", "ueReadAsset(\"AtomReadGeo\", cmd=\"ReadGeo\")")
nuke.menu("Nuke").addCommand(ueMenu+"/nodes/-", "")
nuke.menu("Nuke").addCommand(ueMenu+"/nodes/ueWrite", "ueWriteAsset(\"Write\")")
nuke.menu("Nuke").addCommand(ueMenu+"/nodes/-", "")
nuke.menu("Nuke").addCommand(ueMenu+"/nodes/ueConstant", "ueConstant()")
# Backdrops menu
nuke.menu("Nuke").addCommand(ueMenu+"/backdrops/test",
                             lambda: ueNuke.ueAutoBackdrop("Test", (155, 155, 155, 255)))
nuke.menu("Nuke").addCommand(ueMenu+"/-", "")
# Script utils
nuke.menu("Nuke").addCommand(ueMenu+"/ueRead", ueRead, "ctrl+r")
nuke.menu("Nuke").addCommand(ueMenu+"/ueChecker", ueChecker)
nuke.menu("Nuke").addCommand(ueMenu+"/-", "")
# Render utils
nuke.menu("Nuke").addCommand(ueMenu+"/Render All", "ueNukeRender.ueRender(0)", "F5")
nuke.menu("Nuke").addCommand(ueMenu+"/Render Selected", "ueNukeRender.ueRender(1)", "F7")

nuke.menu("Node Graph").addCommand("ueRead", ueRead)
nuke.menu("Node Graph").addCommand("ueChecker", ueChecker)

# Nodes menu
nuke.menu("Nodes").addCommand("ueTools/ueRead", "ueReadAsset(\"Read\")", "r")
nuke.menu("Nodes").addCommand("ueTools/ueReadGeo", "ueReadAsset(\"ReadGeo\", cmd=\"ReadGeo\")")
nuke.menu("Nodes").addCommand("ueTools/ueAtomReadGeo", "ueReadAsset(\"AtomReadGeo\", cmd=\"ReadGeo\")")
nuke.menu("Nodes").addCommand("ueTools/-", "")
nuke.menu("Nodes").addCommand("ueTools/ueWrite", "ueWriteAsset(\"Write\")", "w")
nuke.menu("Nodes").addCommand("ueTools/-", "")
nuke.menu("Nodes").addCommand("ueTools/ueConstant", "ueConstant()")

# Set new shortcuts for read and write nodes as we're overriding the defaults above
nuke.menu("Nodes").addCommand("Image/Read", "nukescripts.create_read()", "Shift+r", icon="Read.png")
nuke.menu("Nodes").addCommand("Image/Write", "nuke.createNode(\"Write\")", "Shift+w", icon="Write.png")

# Favorites
nuke.addFavoriteDir("asst root", os.getenv("ASST_ROOT"), nuke.ALL)
nuke.addFavoriteDir("render", os.path.join(os.getenv("ASST_ROOT"), "render"), nuke.IMAGE)

# Auto-run
nuke.addOnScriptLoad(nukeChecker)

# Register panels
ueReadPanel = nukescripts.registerWidgetAsPanel("ueNukeRead.ReadPanel", "ueRead", "ue.panel.ueRead", create=True)
ueCheckerPanel = nukescripts.registerWidgetAsPanel("ueNukeChecker.CheckerPanel", "ueChecker", "ue.panel.ueChecker", create=True)

