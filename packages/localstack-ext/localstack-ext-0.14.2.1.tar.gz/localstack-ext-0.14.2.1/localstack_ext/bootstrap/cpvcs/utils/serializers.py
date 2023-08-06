import abc
import logging
import os
from typing import Dict,Optional,Set
from localstack_ext.bootstrap.cpvcs.models import(Commit,CPVCSNode,CPVCSObj,Revision,StateFileRef,Version)
from localstack_ext.bootstrap.cpvcs.utils.common import config_context
LOG=logging.getLogger(__name__)
class CPVCSSerializer(abc.ABC):
 def __init__(self):
  pass
 @abc.abstractmethod
 def store_obj(self,cpvcs_obj:CPVCSObj)->str:
  pass
 @abc.abstractmethod
 def retrieve_obj(self,key:str,remote_path:str=None)->Optional[CPVCSObj]:
  pass
 @staticmethod
 def _deserialize_state_files(state_files_str:str)->Set[StateFileRef]:
  if not state_files_str:
   return set()
  state_files_attrs=state_files_str.split(";")
  state_files:Set[StateFileRef]=set()
  for state_file_attrs in state_files_attrs:
   instance_attrs=list(map(lambda x:x.split(":")[1],state_file_attrs.split(",")))
   state_files.add(StateFileRef(size=int(instance_attrs[0]),service=instance_attrs[1],account_id=instance_attrs[2],region=instance_attrs[3],hash_ref=instance_attrs[4],file_name=instance_attrs[5],rel_path=instance_attrs[6],serialization=instance_attrs[7]))
  return state_files
class VersionSerializerTxt(CPVCSSerializer):
 def store_obj(self,cpvcs_obj:CPVCSNode)->str:
  with open(os.path.join(config_context.get_ver_obj_store_path(),cpvcs_obj.hash_ref),"w")as fp:
   fp.write(str(cpvcs_obj))
  return cpvcs_obj.hash_ref
 def retrieve_obj(self,key:str,remote_path:str=None)->Optional[Version]:
  if remote_path:
   file_path=os.path.join(remote_path,key)
  else:
   file_path=os.path.join(config_context.get_ver_obj_store_path(),key)
  if not os.path.isfile(file_path):
   LOG.debug(f"No Version Obj file found in path {file_path}")
   return
  with open(os.path.join(config_context.get_ver_obj_store_path(),key),"r")as fp:
   lines=list(map(lambda line:line.rstrip(),fp.readlines()))
   version_attrs=list(map(lambda line:line.split("=")[1],lines))
   state_files=self._deserialize_state_files(version_attrs[8])
   return Version(parent_ptr=version_attrs[0],hash_ref=version_attrs[1],creator=version_attrs[2],comment=version_attrs[3],version_number=int(version_attrs[4]),active_revision_ptr=version_attrs[5],outgoing_revision_ptrs=set(version_attrs[6].split(";")),incoming_revision_ptr=version_attrs[7],state_files=state_files)
class RevisionSerializerTxt(CPVCSSerializer):
 def store_obj(self,cpvcs_obj:Revision)->str:
  with open(os.path.join(config_context.get_rev_obj_store_path(),cpvcs_obj.hash_ref),"w")as fp:
   fp.write(str(cpvcs_obj))
  return cpvcs_obj.hash_ref
 def retrieve_obj(self,key:str,remote_path:str=None)->Optional[Revision]:
  file_path=os.path.join(config_context.get_rev_obj_store_path(),key)
  if not os.path.isfile(file_path):
   LOG.debug(f"No Revision Obj file found in path {file_path}")
   return
  def _deserialize_commit(commit_str:str)->Commit:
   if not commit_str or commit_str=="None":
    return
   commit_attrs=list(map(lambda commit_attr:commit_attr.split(":")[1],commit_str.split(",")))
   return Commit(tail_ptr=commit_attrs[0],head_ptr=commit_attrs[1],message=commit_attrs[2],timestamp=commit_attrs[3],delta_log_ptr=commit_attrs[4])
  with open(os.path.join(config_context.get_rev_obj_store_path(),key))as fp:
   lines=list(map(lambda line:line.rstrip(),fp.readlines()))
   revision_attrs=list(map(lambda line:line.split("=")[1],lines))
   state_files=self._deserialize_state_files(revision_attrs[5])
   return Revision(parent_ptr=revision_attrs[0],hash_ref=revision_attrs[1],creator=revision_attrs[2],rid=revision_attrs[3],revision_number=int(revision_attrs[4]),state_files=state_files,assoc_commit=_deserialize_commit(revision_attrs[6]))
version_serializer=VersionSerializerTxt()
revision_serializer=RevisionSerializerTxt()
txt_serializers:Dict[str,CPVCSSerializer]={"version":version_serializer,"revision":revision_serializer}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
