import re
import lyberry_api.channel
from lyberry_api.claim import LBRY_Claim
from lyberry_api.pub import get_channel_from_claim, LBRY_Pub
import lyberry_api.settings

class LBRY_Collection(LBRY_Claim):
    def __init__(self, claim, LBRY_api, channel = {}):
        super(LBRY_Collection, self).__init__(claim, LBRY_api)

        if self.raw["value_type"] != "collection":
            raise ValueError('This is not a collection')
        
        if self.is_repost:
            self.reposter = get_channel_from_claim(self.reposted_raw, LBRY_api)

        self.channel = get_channel_from_claim(claim, LBRY_api)
        self.title = self.raw['value']['title']
        self._claim_ids = self.raw['value']['claims']
        self._claims_feed = False

    def __str__(self):
        return f"LBRY_Collection({self.title})"

    def get_claims_feed(self):
        return self._LBRY_api.claims_from_ids(self._claim_ids)

    def refresh_claims_feed(self):
        self._claims_feed = self.get_claims_feed()

    @property
    def claims_feed(self):
        if not self._claims_feed:
            self.refresh_claims_feed()
        return self._claims_feed

