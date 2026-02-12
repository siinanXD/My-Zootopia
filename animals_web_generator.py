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
    return "".join(serialize_animal(animal) for animal in animals_data)


def get_available_skin_types(animals_data: list[dict]) -> list[str]:
    """Return sorted unique skin_type values found in the JSON."""
    skin_types = set()

    for animal in animals_data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")
        if skin_type:
            skin_types.add(skin_type)

    return sorted(skin_types)


def filter_by_skin_type(animals_data: list[dict], selected_skin_type: str) -> list[dict]:
    """Filter animals that match the selected skin_type (case-insensitive)."""
    selected = selected_skin_type.strip().lower()
    filtered = []

    for animal in animals_data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")

        # Tiere ohne skin_type -> nicht anzeigen
        if not skin_type:
            continue

        if skin_type.strip().lower() == selected:
            filtered.append(animal)

    return filtered


def ask_user_for_skin_type(options: list[str]) -> str:
    """Print options and ask the user to choose one. Repeats until valid."""
    print("Available skin types:")
    for opt in options:
        print(f"- {opt}")

    options_lower = {opt.lower(): opt for opt in options}

    while True:
        user_input = input("\nChoose a skin type from the list: ").strip()
        if user_input.lower() in options_lower:
            return options_lower[user_input.lower()]
        print("Invalid skin type. Please type one exactly from the list.")


def build_animals_page(
    animals_data: list[dict],
    template_path: str = "animals_template.html",
    output_path: str = "animals.html",
) -> None:
    """Create animals.html by filling the template with serialized animals."""
    template_html = load_website(template_path)
    animals_html = get_animals_info(animals_data)
    new_html = template_html.replace("__REPLACE_ANIMALS_INFO__", animals_html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_html)


def main() -> None:
    animals_data = load_data("animals_data.json")

    options = get_available_skin_types(animals_data)
    if not options:
        print("No skin_type values found in the data.")
        return

    selected = ask_user_for_skin_type(options)
    filtered_animals = filter_by_skin_type(animals_data, selected)

    print(f"\nGenerating website for skin_type = {selected} ({len(filtered_animals)} animals).")
    build_animals_page(filtered_animals)


if __name__ == "__main__":
    main()
