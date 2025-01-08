import logging

from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sec_api import QueryApi, RenderApi


class DataHandler:
    def __init__(self, api_key):
        self.query_api = QueryApi(api_key=api_key)
        self.render_api = RenderApi(api_key=api_key)
        logging.basicConfig(level=logging.INFO)

    def get_latest_filings(self, ticker, form_type="10-K", size=5):
        logging.info(f"Fetching latest {size} filings for {ticker}")
        try:
            query = {
                "query": f"ticker:{ticker} AND formType:\"{form_type}\"",
                "from": "0",
                "size": str(size),
                "sort": [{"filedAt": {"order": "desc"}}]
            }
            return self.query_api.get_filings(query).get("filings", [])
        except Exception as e:
            logging.error(f"Error fetching filings: {e}")
            return []

    def extract_filing_content(self, filing):
        url = filing["linkToFilingDetails"]
        date = filing["filedAt"]
        company_name = filing["companyName"]

        try:
            html_content = self.render_api.get_filing(url)
            soup = BeautifulSoup(html_content, "html.parser")
            text = soup.get_text()
            return {
                "page_content": text,
                "metadata": {"company_name": company_name, "date": date, "filing_url": url}
            }
        except Exception as e:
            print(f"Error extracting filing: {e}")
            return None

    def chunk_document(self, text, chunk_size=500):
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=20)
        return splitter.split_text(text)
