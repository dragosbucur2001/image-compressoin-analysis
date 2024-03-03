#!/bin/python3

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# Your client credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIEN_SECRET'

# Create a session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

# Get token for the session
token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
                          client_secret=client_secret, include_client_id=True)


evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: {
      bands: 3,
      sampleType: "AUTO", // default value - scales the output values from [0,1] to [0,255].
    },
  }
}

function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
}
"""

bounding_boxes = [
    [28.822632, 44.48083, 27.870941, 43.841461], # constanta
    [13.822174072265625, 45.85080395917834, 14.55963134765625, 46.29191774991382], # copernicus example
    [25.532227, 44.933696, 24.532471, 45.621722], #mountains
    [23.670044,45.390735, 22.648315,46.019853], # deva
    [23.1427,44.272738, 22.214355,44.887012] # turnu severin
]

request = {
    "input": {
        "bounds": {
            "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
            "bbox": [
                13.822174072265625,
                45.85080395917834,
                14.55963134765625,
                46.29191774991382,
            ],
        },
        "data": [
            {
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": "2022-10-01T00:00:00Z",
                        "to": "2022-10-31T00:00:00Z",
                    }
                },
            }
        ],
    },
    "output": {
        "width": 1024,
        "height": 1024,
    },
    "evalscript": evalscript,
}

length = len(bounding_boxes)
url = "https://sh.dataspace.copernicus.eu/api/v1/process"
for i, bbox in enumerate(bounding_boxes):
    request["input"]["bounds"]["bbox"] = bbox
    print(f"Downloading {i + 1}/{length}")

    response = oauth.post(url, json=request)

    with open(f"png_images/img{i+1}.png", "wb") as f:
        f.write(response.content)

