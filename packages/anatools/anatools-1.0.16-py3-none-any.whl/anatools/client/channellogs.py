"""
Channel Log Functions
"""

def get_channel_runs(self, channelId, datasetId, state=None):
    """Shows all channel run information to the user. Can filter by datasetId and state.
    
    Parameters
    ----------
    channelId : str
        Filter run list on the specific channelId.
    datasetId: str
        Required. Filter run list on the specific datasetId.
    state: str
        Filter run list by status
    
    Returns
    -------
    list[dict]
        List of run associated with datasetId or state.
    """
    if self.check_logout(): return
    runs = self.ana_api.getChannelRuns(channelId=channelId, datasetId=datasetId, state=state)
    if runs:
        return runs
    else: return None       
                

def get_channel_log(self, channelId, workspaceId, runId, loglevel=None):
    """Shows channel log information to the user.
    
    Parameters
    ----------
    channelId : str
        Filter run list on the specific channelId.
    workspaceId: str
        Filter run list on the specific workspaceId.
    runId: str
        Filter run list on the specific runId.
    loglevel: str
        Filter channel log by loglevel
    
    Returns
    -------
    list[dict]
        Get log information by runId
    """
    if self.check_logout(): return
    log = self.ana_api.getChannelLog(channelId=channelId, workspaceId=workspaceId, runId=runId, loglevel=loglevel)
    if log: return log
    else: return None