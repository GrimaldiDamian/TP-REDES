from pydantic import BaseModel, Field
from typing import Optional
import datetime

class Laureate(BaseModel):
    id: int
    firstname: str
    surname: str
    motivation: str
    share: int = Field(ge=1)
    def convertirDict(self):
        return {
            "id": str(self.id),
            "firstname": self.firstname,
            "surname": self.surname,
            "motivation": self.motivation,
            "share": str(self.share)
        }

class Premio(BaseModel):
    anio:int = Field(le = datetime.date.today().year, ge=1901)
    categoria:str
    laureate : list[Laureate]
    overallMotivation : Optional[str] = None
    def convertirDict(self):
        if self.overallMotivation != None:
            return {
                "year": str(self.anio),
                "category": self.categoria,
                "laureates": [laureate.convertirDict() for laureate in self.laureate],
                "overallMotivation": self.overallMotivation
            }
        else:
            return {
                "year": str(self.anio),
                "category": self.categoria,
                "laureates": [laureate.convertirDict() for laureate in self.laureate],
            }