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
    """Serialize a single animal dict into structured HTML."""
    name = animal.get("name")

    locations = animal.get("locations", [])
    location = locations[0] if locations else None

    characteristics = animal.get("characteristics", {})
    diet = characteristics.get("diet")
    animal_type = characteristics.get("type")
    lifespan = characteristics.get("lifespan")
    top_speed = characteristics.get("top_speed")

    def field(label, value):
        if value:
            return f'<li class="card__detail"><strong>{label}:</strong> {value}</li>'
        return ""

    output = ""
    output += '<li class="cards__item">'
    output += f'<div class="card__title">{name}</div>'
    output += '<div class="card__text">'
    output += '<ul class="card__details">'

    output += field("Diet", diet)
    output += field("Location", location)
    output += field("Type", animal_type)
    output += field("Lifespan", lifespan)
    output += field("Top Speed", top_speed)

    output += "</ul>"
    output += "</div>"
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
