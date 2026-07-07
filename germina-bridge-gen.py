import argparse
import json
import os
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

LANGUAGE_MAPPINGS = {
    "cpp": {
        "template": "templates/bundle.hpp.j2",
        "types":{
            "uint8": "uint8_t",
            "uint16": "uint16_t",
            "uint32": "uint32_t",
            "uint64": "uint64_t",
            "int8": "int8_t",
            "int16": "int16_t",
            "int32": "int32_t",
            "int64": "int64_t",
            "float": "float",
        }
    }
}

def main():
    parser = argparse.ArgumentParser(description="Generate C++ bridge code from a JSON manifest (bundle.json).")
    parser.add_argument("target", choices=["cpp"], help="Target language for code generation")
    parser.add_argument("manifest", help="Path to the JSON manifest file.")
    parser.add_argument("output", help="Path to the output C++ header file.")
    args = parser.parse_args()

    with open(args.manifest, 'r') as f:
        manifest = json.load(f)

    config = LANGUAGE_MAPPINGS.get(args.target)
    type_map = config['types']

    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader(SCRIPT_DIR))

    def map_type(type_name):
        return type_map.get(type_name, type_name)

    env.filters['map_type'] = map_type

    template = env.get_template(config['template'])

    output_content = template.render(
        export_types=manifest.get('export', {}).get('types', {}),
        export_methods=manifest.get('export', {}).get('methods', {}),
        generated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        manifest_path=args.manifest
    )
    with open(args.output, 'w') as f:
        f.write(output_content)
    
    print(f"Successfully generated {args.output} for target: {args.target}")

if __name__ == "__main__":
    main()