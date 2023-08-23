from wdcuration import get_quickstatements_for_curated_sheet
from pathlib import Path


HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data").resolve()
RESULTS = HERE.parent.joinpath("results").resolve()


def main():
    qs = get_quickstatements_for_curated_sheet(
        RESULTS / "curation_sheet.csv", "P11954", add_name_as_alias=False
    )
    RESULTS.joinpath("qs.txt").write_text(qs)


if __name__ == "__main__":
    main()
