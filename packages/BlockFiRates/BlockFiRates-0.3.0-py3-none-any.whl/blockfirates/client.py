import cloudscraper
from decimal import Decimal
import json


class BlockFiRates:
    __RATES_URL = "https://blockfi.com/page-data/rates/page-data.json"

    def get_all_rates(self):
scraper = cloudscraper.create_scraper()
html = scraper.get(BlockFiRates.__RATES_URL).content
rate_data = json.loads(html)["result"]["data"]["contentfulComposePage"]["content"]["content"][1]["rowRates"]

        rates = []
        for i in rate_data:
            currency_tier = i["column1Data"]
            currency_name = currency_tier[:currency_tier.find(" ")] if currency_tier.find(" ") > 0 else currency_tier
            currency_rate = i["column3Data"]
            rates.append({
                "Currency": currency_tier,
                "Amount": self._convert_amount_to_rule(i["column2Data"], currency_name),
                "APY": float(Decimal(currency_rate.replace("*", "").rstrip("%"))/100)
            })

        return rates

    def _convert_amount_to_rule(self, AMOUNT, CURRENCY):
        amount = AMOUNT.replace(CURRENCY, "").replace(",", "").strip()

        if amount.find("-") > 0 and amount.find(">") == 0:
            rule = {
                "condition": "between",
                "greater_than": float(amount[:amount.find("-")].replace(">", "").strip()),
                "maximum": float(amount[amount.find("-") + 1:].strip())
            }
        elif amount.find("-") > 0:
            rule = {
                "condition": "between",
                "minimum": float(amount[:amount.find("-")].strip()),
                "maximum": float(amount[amount.find("-") + 1:].strip())
            }
        elif amount.find(">") == 0:
            rule = {
                "condition": "greater than",
                "amount": float(amount.replace(">", "").strip())
            }
        elif amount == "No Limit":
            rule = {
                "condition": "greater than",
                "amount": 0
            }

        return rule

    def get_amount(self, CURRENCY):
        rates = self.get_all_rates()

        return [i for i in rates if i["Currency"] == CURRENCY][0]["Amount"]

    def get_apy(self, CURRENCY):
        rates = self.get_all_rates()

        return [i for i in rates if i["Currency"] == CURRENCY][0]["APY"]
