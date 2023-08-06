"""
Dataset Functions
"""

def get_datasets(self, datasetId=None, name=None, email=None, workspaceId=None):
    """Queries the workspace datasets based off provided parameters. Checks on datasetId, name, owner in this respective order within the specified workspace.
    If only workspace ID is provided, this will return all the datasets in a workspace. 
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to filter.
    name : str 
        Dataset name.   
    email: str
        Owner of the dataset.
    workspaceId : str
        Workspace ID of the dataset's workspace. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        Information about the dataset based off the query parameters provided or a failure message. 
    """
    if self.check_logout(): return
    if datasetId is None: datasetId = ''
    if name is None: name = ''
    if email is None: owner = ''
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getDatasets(workspaceId=workspaceId, datasetId=datasetId, name=name, email=email)


def create_dataset(self, name, graphId, description='', runs=1, priority=1, seed=1, workspaceId=None):
    """Create a new dataset based off an existing staged graph. This will start a new job.
    
    Parameters
    ----------
    name: str
        Name for dataset. 
    graphId : str
        ID of the staged graph to create dataset from.
    description : str 
        Description for new dataset.
    runs : int
        Number of times a channel will run within a single job. This is also how many different images will get created within the dataset. 
    priority : int
        Job priority.
    seed : int
        Seed number.
    workspaceId : str
        Workspace ID of the staged graph's workspace. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        Success or failure message about dataset creation.
    """
    if self.check_logout(): return
    if name is None or graphId is None: return
    if description is None: description = ''
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.createDataset(workspaceId=workspaceId, graphId=graphId, name=name, description=description, runs=runs, seed=seed, priority=priority)


def edit_dataset(self, datasetId, description=None, name=None, workspaceId=None):
    """Update dataset description.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to update description for.
    description : str 
        New description.
    name: str
        New name for dataset.
    workspaceId : str
        Workspace ID of the dataset to get updated. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        Success or failure message about dataset update.
    """
    if self.check_logout(): return
    if datasetId is None: return
    if workspaceId is None: workspaceId = self.workspace
    if name is None and description is None: return
    return self.ana_api.editDataset(workspaceId=workspaceId, datasetId=datasetId, name=name, description=description)
    

def delete_dataset(self, datasetId, workspaceId=None):
    """Delete an existing dataset.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID of dataset to delete.
    workspaceId : str
        Workspace ID that the dataset is in. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        Success or failure message about dataset deletion.
    """
    if self.check_logout(): return
    if datasetId is None: return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.deleteDataset(workspaceId=workspaceId, datasetId=datasetId)
    

def download_dataset(self, datasetId, workspaceId=None, localDir=None):
    """Download a dataset.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID of dataset to download.
    workspaceId : str
        Workspace ID that the dataset is in. If none is provided, the default workspace will get used. 
    
    Returns
    -------
    str
        Success or failure message about dataset download.
    """
    import requests, os
    if self.check_logout(): return
    if datasetId is None: datasetId
    if workspaceId is None: workspaceId = self.workspace
    if localDir is None: localDir = os.getcwd()
    elif not os.path.exists(localDir): raise Exception(f"Could not find directory {localDir}.")
    url = self.ana_api.downloadDataset(workspaceId=workspaceId, datasetId=datasetId)        
    fname = url.split('?')[0].split('/')[-1]
    with requests.get(url, stream=True) as downloadresponse:
        downloadresponse.raise_for_status()
        with open(os.path.join(localDir,fname), 'wb') as f:
            for chunk in downloadresponse.iter_content(chunk_size=8192): f.write(chunk)
    return os.path.join(localDir,fname)


def cancel_dataset(self, datasetId, workspaceId=None):
    """Stop a running job.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID of the running job to stop.
    workspaceId: str
        Workspace ID of the running job. If none is provided, the default workspace will get used. 
    
    Returns
    -------
    str
        Success or error message about stopping the job execution.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.cancelDataset(workspaceId=workspaceId, datasetId=datasetId)

def upload_dataset(self, filename, description=None, workspaceId=None):
    """Uploads user dataset. 
    
    Parameters
    ----------
    workspaceId : str
    description : str
    name: str
    
    Returns
    -------
    str
        success
    """
    import requests
    if self.check_logout(): return
    if filename is None: raise ValueError("Filename must be defined.")
    if description is None: description = ''
    if workspaceId is None: workspaceId = self.workspace
    fileinfo = self.ana_api.datasetUpload( workspaceId=workspaceId, filename=filename, description=description)
    datasetId = fileinfo['key'].split('/')[-1].split('.')[0]
    with open(filename, 'rb') as filebytes:
        files = {'file': filebytes}
        data = {
            "key":                  fileinfo['fields']['key'],
            "bucket":               fileinfo['fields']['bucket'],
            "X-Amz-Algorithm":      fileinfo['fields']['algorithm'],
            "X-Amz-Credential":     fileinfo['fields']['credential'],
            "X-Amz-Date":           fileinfo['fields']['date'],
            "X-Amz-Security-Token": fileinfo['fields']['token'],
            "Policy":               fileinfo['fields']['policy'],
            "X-Amz-Signature":      fileinfo['fields']['signature'],
        }
        response = requests.post(fileinfo['url'], data=data, files=files)
        if response.status_code != 204: 
            print(f'Failed to upload dataset, with status code: {response.status_code}')
            return False
    return datasetId
