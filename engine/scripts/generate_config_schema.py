import json
import pathlib
from pydantic import TypeAdapter
from engine.config.models import EngineConfig


def generate_config_schema():
    # Define paths
    project_root = pathlib.Path(__file__).parent.parent.parent
    schema_dir = project_root / "schemas"
    schema_file = schema_dir / "engine_config_schema.json"

    # Ensure schema directory exists
    schema_dir.mkdir(exist_ok=True)

    # Use Pydantic's TypeAdapter to extract the schema from the Dataclass
    adapter = TypeAdapter(EngineConfig)
    schema_dict = adapter.json_schema()

    # Add a title and description for the IDE tooltip
    schema_dict["title"] = "Blackbox Engine Configuration"
    schema_dict["description"] = "Schema for validating engine.toml and engine.json"

    # Write to disk
    with open(schema_file, "w") as f:
        json.dump(schema_dict, f, indent=4)

    print(f"✅ Schema generated at: {schema_file}")
    print(
        f"💡 Add this to the top of your TOML: #:schema ./schemas/engine_config_schema.json"
    )


if __name__ == "__main__":
    generate_config_schema()
