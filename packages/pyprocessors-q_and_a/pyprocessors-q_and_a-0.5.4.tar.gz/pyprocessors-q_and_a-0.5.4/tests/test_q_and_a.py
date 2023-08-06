import json
from pathlib import Path
from typing import List

from pymultirole_plugins.v1.schema import Document
from pyprocessors_q_and_a.q_and_a import (
    QandAProcessor,
    QandAParameters,
    TrfModel,
    ProcessingUnit,
)


def test_q_and_a_french_segments():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/questions.json")
    with source.open("r") as fin:
        data = json.load(fin)
        parameters = QandAParameters(
            model=TrfModel.camembert_base_squadFR_fquad_piaf,
            processing_unit=ProcessingUnit.segment,
        )
        annotator = QandAProcessor()
        docs: List[Document] = annotator.process([Document(**data)], parameters)
        result = Path(testdir, "data/answers.json")
        with result.open("w") as fout:
            json.dump(docs[0].dict(), fout, indent=2)
