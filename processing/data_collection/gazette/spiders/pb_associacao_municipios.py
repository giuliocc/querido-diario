from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class PbAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "pb_associacao_municipios"
    TERRITORY_ID = "2500000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/famup"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/famup/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/famup/materia/calendario/extra"
    )
