import os

# Locate the 1HSG file
possible_paths = [
    "data/1HSG.cif",
    "data/01_Protein/1HSG.cif",
    "1HSG.cif"
]

cif_file = None
for path in possible_paths:
    if os.path.exists(path):
        cif_file = path
        break

if not cif_file:
    print("Error: 1HSG.cif file not found! Please check the path.")
    exit(1)

print(f"[SUCCESS] File found: {cif_file}\n")

# Inspect and count structure components
atom_count = 0
hetatm_count = 0
water_count = 0
chains = set()

with open(cif_file, "r") as f:
    for line in f:
        if line.startswith("ATOM"):
            atom_count += 1
            parts = line.split()
            if len(parts) > 6:
                chains.add(parts[6])  # Collect Chain ID
        elif line.startswith("HETATM"):
            hetatm_count += 1
            if "HOH" in line:
                water_count += 1

# Print summary to terminal
print("--- 1HSG Structure Validation Summary ---")
print(f"Total Protein Atoms (ATOM)    : {atom_count}")
print(f"Total Non-Protein Atoms (HETATM): {hetatm_count}")
print(f"Water Molecules (HOH) to remove : {water_count}")
print(f"Detected Chains               : {', '.join(sorted(chains))}")
print("-----------------------------------------")

# Save output report to the results folder
os.makedirs("results", exist_ok=True)
report_path = "results/protein_inspection_report.txt"

with open(report_path, "w") as out:
    out.write("--- 1HSG Structure Validation Report ---\n")
    out.write(f"Inspected File    : {cif_file}\n")
    out.write(f"Protein Atoms     : {atom_count}\n")
    out.write(f"HETATM Records    : {hetatm_count}\n")
    out.write(f"Water Molecules   : {water_count}\n")
    out.write(f"Chains            : {', '.join(sorted(chains))}\n")

print(f"\n[SAVED] Report created: {report_path}")
