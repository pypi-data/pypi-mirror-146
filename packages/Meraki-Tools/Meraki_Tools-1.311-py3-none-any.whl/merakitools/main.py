"""
    Main Module of autosync Application
"""
import asyncio
from os import getenv
from merakitools import meraki_tasks
from merakitools import const, lib, model, utils
from merakitools.model import golden_nets, meraki_nets


def setup_app(cfg_file=None):
	const.appcfg = model.APPCONFIG(cfg_file)
	temp_sdk = lib.MerakiApi()
	const.meraki_sdk = temp_sdk.api
def start(suppresslogging=None, merakiapikey=None, write=None, allorgs=None, autosyncorgs=None,
          usecache=None, cachetimeout=None, goldentag=None, targettag=None, tagoverride=None,
          logginglevel=None,configfile=None,debug=None,networkname=None):
	cfg = {'suppress_logging'        : suppresslogging,
	       'MERAKI_DASHBOARD_API_KEY': merakiapikey,
	       'write'                   : write,
	       'whitelist'               : autosyncorgs,
	       'tag_golden'              : goldentag,
	       'tag_target'              : targettag,
	       'all_orgs'                : allorgs,
	       'use_cache'               : usecache,
	       'cache_timeout'           : cachetimeout,
	       'tag_override'            : tagoverride,
	       'logging_level'           : logginglevel,
	       'debug'                   : debug}
	return cfg

def run(cfg_file=None,task='sync',device_task=None,network_name=None,config_overide=None):
	"""
    Main Module Start of Application
    Args:
    Returns:

    """
	setup_app(cfg_file)
	if config_overide is not None:
		const_config = getattr(const, "appcfg")
		for config_item in config_overide.keys():
			if config_overide[config_item] is not None:
				if config_item == "network_tags":
					tag_list = getattr(const_config,config_item)
					tag_list.append(config_overide[config_item])
				else:
					setattr(const_config,config_item,config_overide[config_item])
		
	if task == 'sync':
		finish = asyncio.run(meraki_tasks.sync_task(network_name=network_name))
		return finish
	elif task == 'device_config':
		asyncio.run(meraki_tasks.device_config(device_task))
	
	

if __name__ == '__main__':
	#config_file = '~/apps/testSync/ciscolab-config.json'
	config_file=None
	network_name = "29Q892"
	if config_file is None:
		config_file = getenv("MERAKI_TOOLS_CONFIG", None)
	#run(config_file,"sync",network_name="29Q892")
	cfg_overide = start(targettag="test")
	run(config_file,"sync",network_name="29Q892,09X055,07X018,15B029,15B094,02M041",config_overide=cfg_overide)
	#run(config_file, "sync")
	print('Done')
