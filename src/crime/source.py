# Maintainer:     Ryan Young
# Last Modified:  May 10, 2022
from dataclasses import dataclass
import pandas as pd
from crime.soda_api import Soda



@dataclass
class Source:

    id: str
    base_url: str
    __data: pd.DataFrame = None
    __metadata: dict = None

    @property
    def data(self) -> pd.DataFrame:
        ...

    @property
    def head(self) -> pd.DataFrame:
        ...

    def load(self, **kwargs):
        ...

    @property
    def metadata(self):
        ...

    @property
    def columns(self):
        ...
        

