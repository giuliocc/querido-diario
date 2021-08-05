import datetime
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjPetropolisSpider(BaseGazetteSpider):
    name = "rj_petropolis"
    TERRITORY_ID = "3303906"
    allowed_domains = ["petropolis.rj.gov.br"]
    start_date = datetime.date(2001, 10, 2)
    start_urls = [
        "https://www.petropolis.rj.gov.br/pmp/index.php/servicos-na-web/informacoes/diario-oficial/viewcategory/3-diario-oficial.html"
    ]

    def parse(self, response):
        raw_links = response.xpath("//select[@id='cat_list']/@onchange").get()
        links = re.findall(r"/pmp/[\w\d\-\./]+html", raw_links)
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_editions)

    def parse_editions(self, response):
        editions = response.xpath("//table[contains(.//a/@title, 'Download')]")
        for edition in editions:
            link = edition.xpath("./tr[1]/td/b/a/@href").get()
            raw_edition_number = edition.xpath("./tr[2]/td/p/strong[1]/text()").get()
            edition_number = re.search(r"Nº\s+(\d+)", raw_edition_number).group(1)
            raw_date = edition.xpath("./tr[2]/td/p/strong[2]/text()").get().strip()
            date = datetime.datetime.strptime(raw_date, "%d/%m/%Y").date()

            yield Gazette(
                date=date,
                edition_number=edition_number,
                file_urls=[response.urljoin(link)],
                power="executive",
            )
