import xml.etree.ElementTree as ET
import sys

def check_visual_collision(sdf_file):
    tree = ET.parse(sdf_file)
    root = tree.getroot()

    # Namespace handling if needed
    ns = {'sdf': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}

    # Find all links
    links = root.findall('.//link', ns)
    if not links:
        print("No <link> elements found in the SDF.")
        return

    # Store info: {link_name: {visuals: {name: uri}, collisions: {name: uri}}}
    report = {}

    for link in links:
        link_name = link.attrib.get('name', 'unnamed_link')
        visuals = {}
        collisions = {}

        # Extract visuals
        for visual in link.findall('visual', ns):
            vname = visual.attrib.get('name', 'unnamed_visual')
            mesh_uri = None
            mesh = visual.find('.//mesh', ns)
            if mesh is not None:
                uri = mesh.find('uri', ns)
                if uri is not None:
                    mesh_uri = uri.text.strip()
            visuals[vname] = mesh_uri

        # Extract collisions
        for collision in link.findall('collision', ns):
            cname = collision.attrib.get('name', 'unnamed_collision')
            mesh_uri = None
            mesh = collision.find('.//mesh', ns)
            if mesh is not None:
                uri = mesh.find('uri', ns)
                if uri is not None:
                    mesh_uri = uri.text.strip()
            collisions[cname] = mesh_uri

        report[link_name] = {'visuals': visuals, 'collisions': collisions}

    # Now analyze report
    print(f"Checked {len(report)} links.\n")
    for link_name, content in report.items():
        visuals = content['visuals']
        collisions = content['collisions']

        print(f"Link: {link_name}")
        print(f"  Visuals ({len(visuals)}):")
        for vname, vuri in visuals.items():
            print(f"    Visual '{vname}': mesh URI = '{vuri}'")

        print(f"  Collisions ({len(collisions)}):")
        for cname, curi in collisions.items():
            print(f"    Collision '{cname}': mesh URI = '{curi}'")

        # Check for visuals without matching collision by name pattern
        missing_collision = []
        for vname in visuals.keys():
            # Try to find collision with matching name or similar
            if vname not in collisions:
                missing_collision.append(vname)

        if missing_collision:
            print(f"  >> WARNING: Visuals without matching collision: {missing_collision}")
        else:
            print("  All visuals have matching collisions (by name).")

        print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_sdf_collision.py path/to/model.sdf")
        sys.exit(1)

    sdf_path = sys.argv[1]
    check_visual_collision(sdf_path)
