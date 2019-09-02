import urequests

class AllThingsTalkDevice:
    def __init__(self, device_id, device_token):
        self.url = "https://api.allthingstalk.io/device/{}/state".format(device_id)
        self.headers = {"Authorization": "Bearer {}".format(device_token), 
                        "Content-type": "application/json", }

    def set_asset_state(self, asset_name, asset_state):
        data = {asset_name:{"value":asset_state}}
        request = urequests.put(self.url, headers=self.headers, json=data)
        request.close()

    def set_multiple(self, asset_states):
        data = {}
        for key in asset_states:
            asset_states[key] = {"value":asset_states[key]}
