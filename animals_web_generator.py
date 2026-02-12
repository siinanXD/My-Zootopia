import json

def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)


animals_data = load_data('animals_data.json')


def get_animals_info(animals_data):
    """
    summarize Name,Location,Diet,Type

    """
    for animal in animals_data:
        animal_name = animal["name"]
        animal_location = animal["locations"][0]
        animal_diet = animal["characteristics"]["diet"]
        animal_type = animal["characteristics"].get("type")


        print(f"Name: {animal_name}")
        print(f"Diet: {animal_diet}")
        print(f"Location: {animal_location}")
        if animal_type:
            print(f"Type: {animal_type}")

        print()


get_animals_info(animals_data)



