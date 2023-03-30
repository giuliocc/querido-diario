import datetime as dt

from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.spiders.base.dosp import DospGazetteSpider


class MgUberabaSpider(DospGazetteSpider):
    TERRITORY_ID = "3170107"
    name = "mg_uberaba_main"

    code = 2364
    start_date = dt.date(2021, 9, 1)


class MgUberaba2003To2021Spider(BaseGazetteSpider):
    TERRITORY_ID = "3170107"
    name = "mg_uberaba_2003_2021"
    start_date = dt.date(2003, 4, 25)
    end_date = dt.date(2021, 9, 2)

    def start_requests(self):
        for year in range(self.start_date.year, self.end_date.year + 1):
            yield FormRequest(
                url="http://www.uberaba.mg.gov.br/portal/listImagesHtml",
                method="POST",
                formdata={
                    "desc": "1",
                    "type": "1",
                    "folder": f"portavoz/arquivos/{year}",
                    "limit": "5000",
                    "page": "1",
                    "types": "gif,jpg,png,bmp,tif,dxf,swf,dcr,mov,qt,ram,rm,avi,mpg,mpeg,asf,flv,pdf,doc,docx,xls,xlsx,zip,rar,txt,cdr,ai,eps,ppt,pptx,pot,psd,wmv",
                    "listAll": "1",
                },
                cb_kwargs={"start_date": self.start_date, "end_date": self.end_date},
            )

    def parse(self, response, start_date, end_date):
        gazettes = response.css(".claGaleriaBoxFileTable")
        for gazette in gazettes:
            raw_date = gazette.css("::text").re_first(r"(\d{2}-\d{2}-\d{4})")
            gazette_date = dt.datetime.strptime(raw_date, "%d-%m-%Y").date()
            if gazette_date < start_date or gazette_date > end_date:
                continue

            gazette_url = response.urljoin(
                gazette.css("img::attr(onclick)").re_first(r"download\(\'(.*)\'\)")
            )
            edition_number = gazette.css("::text").re_first(r"^\s*?(\d{4})")

            yield Gazette(
                date=gazette_date,
                file_urls=[
                    gazette_url,
                ],
                is_extra_edition=False,
                edition_number=edition_number,
                power="executive_legislative",
            )
