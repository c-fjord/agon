from models.activities import Sex


def sex_translator(sex: str) -> Sex:
    if sex.lower() == "male":
        return Sex.MALE
    elif sex.lower() == "femal":
        return Sex.FEMAL
    else:
        return Sex.OTHER
