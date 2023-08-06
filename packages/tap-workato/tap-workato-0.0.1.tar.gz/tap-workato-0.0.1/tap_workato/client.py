"""REST client handling, including WorkatoStream base class."""

from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class WorkatoStream(RESTStream):
    """Workato stream class."""

    url_base = "https://www.workato.com"

    records_jsonpath = "$[*]"
    current_page = None

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        return {
            "x-user-token": self.config.get("user_token"),
            "x-user-email": self.config.get("user_email"),
        }

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        next_page_token: Optional[int] = None
        if self.current_page:
            all_matches = extract_jsonpath(self.records_jsonpath, response.json())
            records_cnt = sum([1 for m in all_matches])
            next_page_token = self.current_page + 1 if records_cnt == 100 else None

        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {"per_page": 100}
        if next_page_token:
            params["page"] = next_page_token
            self.current_page = next_page_token
        if self.replication_key:
            params["order"] = "default"
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        """As needed, append or transform raw data to match expected structure."""
        return row
