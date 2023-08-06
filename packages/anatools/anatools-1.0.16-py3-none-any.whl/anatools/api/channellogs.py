"""
Channels Logs API calls.
"""

def getChannelRuns(self, channelId, datasetId, state=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getChannelRuns",
            "variables": {
                "channelId": channelId,
                "datasetId": datasetId,
                "state": state,
            },
            "query": """query 
                getChannelRuns($channelId: String!, $datasetId: String!, $state: String) {
                    getChannelRuns(channelId: $channelId, datasetId: $datasetId, state: $state) {
                        runId
                        workspaceId
                        datasetId
                        channelId
                        startTime
                        endTime
                        state
                    }
                }"""})
    return self.errorhandler(response, "getChannelRuns")


def getChannelLog(self, channelId, workspaceId, runId, loglevel=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getChannelLog",
            "variables": {
                "channelId": channelId,
                "workspaceId": workspaceId,
                "runId": runId,
                "loglevel": loglevel,
            },
            "query": """query 
                getChannelLog($channelId: String!, $workspaceId: String!, $runId: String!, $loglevel: String) {
                    getChannelLog(channelId: $channelId, workspaceId: $workspaceId, runId: $runId, loglevel: $loglevel) {
                        runId
                        channelId
                        organizationId
                        workspaceId
                        datasetId
                        datasetSeed
                        datasetRun
                        startTime
                        endTime
                        state
                        email
                        graph
                        log
                    }
                }"""})
    return self.errorhandler(response, "getChannelLog")