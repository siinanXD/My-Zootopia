import json


def load_data(file_path: str):
    """Load a JSON file and return the parsed data."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_website(html_path: str) -> str:
    """Load an HTML file and return its content as a string."""
    with open(html_path, "r", encoding="utf-8") as web:
        return web.read()


def serialize_animal(animal: dict) -> str:
    """Serialize a single animal dict into an extended HTML card."""
    name = animal.get("name")

    locations = animal.get("locations", [])
    location = locations[0] if locations else None

    taxonomy = animal.get("taxonomy", {})
    scientific_name = taxonomy.get("scientific_name")

    characteristics = animal.get("characteristics", {})
    diet = characteristics.get("diet")
    animal_type = characteristics.get("type")
    lifespan = characteristics.get("lifespan")
    top_speed = characteristics.get("top_speed")
    weight = characteristics.get("weight")
    habitat = characteristics.get("habitat")
    color = characteristics.get("color")

    def field(label, value):
        return f"<strong>{label}:</strong> {value}<br/>" if value else ""

    output = ""
    output += '<li class="cards__item">'
    output += f'<div class="card__title">{name}</div>'
    output += '<p class="card__text">'

    output += field("Scientific Name", scientific_name)
    output += field("Diet", diet)
    output += field("Location", location)
    output += field("Type", animal_type)
    output += field("Habitat", habitat)
    output += field("Top Speed", top_speed)
    output += field("Weight", weight)
    output += field("Lifespan", lifespan)
    output += field("Color", color)

    output += "</p>"
    output += "</li>"

    return output



def get_animals_info(animals_data: list[dict]) -> str:
    """Build the full HTML string for all animals."""
    animals_info = ""
    for animal in animals_data:
        animals_info += serialize_animal(animal)
    return animals_info


def build_animals_page(
        data_path: str = "animals_data.json",
    template_path: str = "animals_template.html",
    output_path: str = "animals.html",
) -> None:
    """Create animals.html by filling the template with serialized animals."""
    animals_data = load_data(data_path)
    template_html = load_website(template_path)

    animals_html = get_animals_info(animals_data)
    new_html = template_html.replace("__REPLACE_ANIMALS_INFO__", animals_html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_html)


if __name__ == "__main__":
    build_animals_page()
