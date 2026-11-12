import os

os.makedirs("data/01_Protein", exist_ok=True)

possible_paths = ["1HSG.cif", "data/1HSG.cif", "data/01_Protein/1HSG.cif"]
cif_path = next((p for p in possible_paths if os.path.exists(p)), None)

if not cif_path:
    print("Error: 1HSG.cif not found!")
    exit(1)

print(f"Loading structure from: {cif_path}")

protein_lines = []
ligand_lines = []

with open(cif_path, 'r') as f:
    for line in f:
        # Simple parsing for ATOM (protein) and HETATM (ligand/water)
        if line.startswith("ATOM"):
            protein_lines.append(line)
        elif line.startswith("HETATM") and "HOH" not in line:
            ligand_lines.append(line)

# Convert CIF ATOM/HETATM records to basic PDB format lines
def convert_to_pdb_format(lines, output_path):
    with open(output_path, 'w') as out:
        for i, line in enumerate(lines):
            parts = line.split()
            if len(parts) < 10:
                continue
            # Basic reformatting to PDB ATOM/HETATM record
            record_name = parts[0]
            atom_name = parts[2]
            res_name = parts[5]
            chain_id = parts[6]
            res_seq = parts[7]
            x, y, z = parts[10], parts[11], parts[12]
            element = parts[-1]
            
            pdb_line = f"{record_name:<6}{i+1:>5} {atom_name:<4} {res_name:>3} {chain_id:>1}{res_seq:>4}    {x:>8}{y:>8}{z:>8}  1.00 20.00          {element:>2}\n"
            out.write(pdb_line)
        out.write("END\n")

convert_to_pdb_format(protein_lines, "data/01_Protein/1hsg_protein.pdb")
convert_to_pdb_format(ligand_lines, "data/01_Protein/1hsg_ligand.pdb")

print("\n[SUCCESS] Cleaning and extraction complete!")