import json
import logging
import random
import string
import sys
import traceback
from typing import Dict

import requests
from requests.structures import CaseInsensitiveDict

from fuzzing_cli.fuzz.scribble import ScribbleMixin

from .exceptions import (
    AuthorizationError,
    BadStatusCode,
    PayloadError,
    RequestError,
    ScribbleMetaError,
)
from .ide.generic import IDEArtifacts

LOGGER = logging.getLogger("fuzzing-cli")


class FaasClient:
    """ A client to interact with the FaaS API.

    This object receives solidity compilation artifacts and a Harvey Seed state, generates a payload that the faas
    API can consume and submits it, also triggering the start of a Campaign.
    """

    def __init__(
        self,
        faas_url,
        campaign_name_prefix,
        project_type,
        api_key,
        client_id,
        refresh_token,
        auth_endpoint,
        project,
        time_limit,
    ):
        self.faas_url = faas_url
        self.campaign_name_prefix = campaign_name_prefix
        self.project_type = project_type
        self.project = project

        self._api_key = api_key
        self._client_id = client_id
        self._refresh_token = refresh_token
        self._auth_endpoint = auth_endpoint
        self.time_limit = time_limit

    @property
    def headers(self):
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer " + str(self.api_key)
        return headers

    @property
    def api_key(self):
        if self._api_key:
            return self._api_key

        response = requests.post(
            f"https://{self._auth_endpoint}/oauth/token",
            data={
                "grant_type": "refresh_token",
                "client_id": self._client_id,
                "refresh_token": self._refresh_token,
            },
        )
        body = response.json()
        if response.status_code != 200:
            error = body.get("error", "")
            description = body.get("error_description", "")
            raise AuthorizationError(
                f"Authorization failed. Error: {error}", detail=description
            )
        return body.get("access_token")

    def generate_campaign_name(self):
        """Return a random name with the provided prefix self.campaign_name_prefix."""
        letters = string.ascii_lowercase
        random_string = "".join(random.choice(letters) for i in range(5))
        return str(self.campaign_name_prefix + "_" + random_string)

    def start_faas_campaign(self, payload):
        """Make HTTP request to the faas"""
        try:
            req_url = f"{self.faas_url}/api/campaigns/?start_immediately=true"
            h = self.headers
            response = requests.post(req_url, json=payload, headers=h)
            response_data = response.json()
            if response.status_code != requests.codes.ok:
                if (
                    response.status_code == 403
                    and response_data["detail"]
                    and response_data["error"] == "SubscriptionError"
                ):
                    raise BadStatusCode("Subscription Error", response_data["detail"])

                else:
                    raise BadStatusCode(
                        f"Got http status code {response.status_code} for request {req_url}",
                        detail=response_data["detail"],
                    )
            return response_data["id"]
        except Exception as e:
            if isinstance(e, BadStatusCode):
                raise e
            raise RequestError("Error starting FaaS campaign", detail=str(e))

    def create_faas_campaign(
        self,
        campaign_data: IDEArtifacts,
        seed_state: Dict[str, any],
        dry_run: bool = False,
    ):
        """Submit a campaign to the FaaS and start that campaign.

        This function takes a FaaS payload and makes an HTTP request to the Faas backend, which
        then creates and starts a campaign. The campaign is started because of the `start_immediately=true` query
        parameter.

        This will send the following data to the FaaS for analysis:

        * :code:`name`
        * :code:`parameters` A dict of Harvey configuration options
        * :code:`sources` A dict containing source files code and AST
        * :code:`contracts` Solidity artifacts of the target smart contracts
        * :code:`corpus` Seed state of the target contract. Usually the list of transactions that took place on the
        local ganache (or equivalent) instance.

        :return: Campaign ID
        """
        try:
            api_payload_params = {
                "discovery-probability-threshold": seed_state[
                    "discovery-probability-threshold"
                ],
                "num-cores": seed_state["num-cores"],
                "assertion-checking-mode": seed_state["assertion-checking-mode"],
            }
            api_payload = {
                "parameters": api_payload_params,
                "name": self.generate_campaign_name(),
                "corpus": seed_state["analysis-setup"],
                "sources": campaign_data.sources,
                "contracts": campaign_data.contracts,
                "project": self.project
            }
            if self.time_limit:
                api_payload["timeLimit"] = self.time_limit

        except KeyError as e:
            raise PayloadError(
                "Error extracting data from payload", detail=f"Key {str(e)} not found"
            )

        try:
            instr_meta = ScribbleMixin.get_arming_instr_meta()
            if instr_meta is not None:
                api_payload["instrumentationMetadata"] = instr_meta
        except Exception as e:
            raise ScribbleMetaError(
                "Error getting Scribble arming metadata.", detail=str(e)
            )

        if dry_run:
            print("Printing output \n --------")
            print(f"{json.dumps(api_payload)}")
            print("End of output \n --------")
            return "campaign not started due to --dry-run option"

        campaign_id = self.start_faas_campaign(api_payload)

        return campaign_id
