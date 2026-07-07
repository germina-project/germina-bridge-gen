import argparse
import json
import os
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

LANGUAGE_MAPPINGS = {
    "cpp": {
        "template": "templates/bundle.hpp.j2",
        "extension": ".hpp",
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
    parser.add_argument("output", help="Path to the output directory or file.")
    args = parser.parse_args()

    with open(args.manifest, 'r') as f:
        manifest = json.load(f)

    config = LANGUAGE_MAPPINGS.get(args.target)
    type_map = config['types']
    target_ext = config['extension']

    bundle_name = manifest.get('name', 'bundle')
    output_path = args.output

    if os.path.isdir(output_path) or not os.path.splitext(output_path)[1]:
        os.makedirs(output_path, exist_ok=True)
        output_path = os.path.join(output_path, f"{bundle_name}_bridge{target_ext}")

    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader(SCRIPT_DIR))

    def map_type(type_name):
        return type_map.get(type_name, type_name)

    env.filters['map_type'] = map_type

    template = env.get_template(config['template'])

    output_content = template.render(
        export_types=manifest.get('export', {}).get('types', {}),
        export_methods=manifest.get('export', {}).get('methods', {}),
        import_types=manifest.get('import', {}).get('types', {}),
        import_methods=manifest.get('import', {}).get('methods', {}),
        requirements=manifest.get('requirements', []),
        generated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        author=manifest.get('author', 'Unknown'),
        mount=manifest.get('mount', f"{bundle_name}_mount"),
        unmount=manifest.get('unmount', ''),
        manifest_path=args.manifest
    )
    with open(output_path, 'w') as f:
        f.write(output_content)

    print(f"Successfully generated {output_path} for target: {args.target}")

if __name__ == "__main__":
    main()