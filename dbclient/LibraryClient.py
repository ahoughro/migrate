import time, json
from dbclient import *

class LibraryClient(dbclient):

  def get_cluster_list(self, alive = True):
    """ Returns an array of json objects for the running clusters. Grab the cluster_name or cluster_id """
    cl = self.get("/clusters/list", printJson = False)
    if alive:
      running = filter(lambda x: x['state'] == "RUNNING", cl['clusters'])
      return list(running)
    else:
      return cl['clusters']

  def log_library_details(self, libs_log='logs/lib_details.log'):
    all_libs = self.get('/libraries/list', version='1.2')
    with open(libs_log, "w") as fp:
      for x in all_libs:
        lib_details = self.get('/libraries/status?libraryId={0}'.format(x['id']), version='1.2')
        fp.write(json.dumps(lib_details) + '\n')

  def log_cluster_libs(self, cl_lib_log='logs/attached_cluster_libs.log'):
    cl = self.get_cluster_list(False)
    with open(cl_lib_log, "w") as fp:
      for x in cl:
        cid = x['cluster_id']
        libs = self.get("/libraries/cluster-status?cluster_id={0}".format(cid))
        fp.write(json.dumps(libs))
        fp.write("\n") 