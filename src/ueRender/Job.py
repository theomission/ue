import os, sys
import json, time

import drqueue.base.libdrqueue as drqueue

import ueSpec

import ueCore.AssetUtils as ueAssetUtils

class Job():
    def __init__(self, sourceSpec, destSpec, run, frame_start=1, frame_end=1, priority=10, **kargs):
        self.sourceSpec = sourceSpec
        self.destSpec = destSpec
        self.run = run
        self.frame_start = frame_start
        self.frame_end = frame_end
        self.priority = priority
        self.options = kargs

    def createScript(self):
        job = {}

        if self.run == "nuke":
            ext = "nk"

        proj = ueAssetUtils.getProject(self.destSpec)
        asst = ueAssetUtils.getAsset(self.destSpec)

        versions = ueAssetUtils.getVersions(self.sourceSpec)
        version = versions[len(versions)-1]

        p = os.path.join(version["path"], version["file_name"]+"."+ext)

        for f in range(self.frame_start, self.frame_end+1):
            frame = {}
            if self.run == "nuke":
                frame["cmd"] = "nuke -x -V -f -X %s -F %i-%i %s" % (",".join(self.options["writeNode"]),
                                                                    f, f, p)
            frame["proj"] = self.destSpec.proj
            frame["grp"] = self.destSpec.grp
            frame["asst"] = self.destSpec.asst
            frame["proj_root"] = proj["path"]
            frame["asst_root"] = asst["path"]
            job[f] = frame

        versions = ueAssetUtils.getVersions(self.destSpec)
        version = versions[len(versions)-1]

        p = os.path.join(asst["path"], "tmp", "drQueue", version["file_name"]+"."+str(int(time.time()))+".dq")

        if not os.path.exists(os.path.dirname(p)):
            import ueCore.FileUtils as ueFileUtils
            ueFileUtils.createDir(os.path.dirname(p))

        try:
            f = open(p, "w")
            f.write(json.dumps(job, sort_keys=True, indent=4))
            f.close()
        except IOError, e:
            print "ERROR: Creating job script '%s' (%s)" % (p, e)
            sys.exit(2)

        self.script = p

    def spool(self):
        p = os.path.join(os.getenv("UE_PATH"), "src", "ueRender", "Runner.py")

        job = drqueue.job()

        job.name = str(self.destSpec)
        job.frame_start = self.frame_start
        job.frame_end = self.frame_end
        job.cmd = str("python %s %s" % (p, self.script))
        job.priority = self.priority

        return job.send_to_queue()

