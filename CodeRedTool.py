import arcpy
import os

def main():
    # === Script tool inputs ===
    input_layer = arcpy.GetParameter(0)      # Feature layer from map
    output_folder = arcpy.GetParameterAsText(1)
    output_name = arcpy.GetParameterAsText(2)

    # Hardcoded NAD83 (EPSG:4269)
    output_sr = arcpy.SpatialReference(4269)

    # Validate selection
    desc = arcpy.Describe(input_layer)
    if not desc.FIDSet:
        arcpy.AddError("⚠️ No features are selected in the input layer.")
        raise ValueError("No features selected.")

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = "in_memory"

    # Copy selected features
    arcpy.AddMessage("Copying selected features...")
    temp_fc = "in_memory/selected_features"
    arcpy.CopyFeatures_management(input_layer, temp_fc)

    # Reproject to NAD83
    arcpy.AddMessage("Reprojecting to NAD83 (EPSG:4269)...")
    projected_fc = "in_memory/projected_features"
    arcpy.Project_management(temp_fc, projected_fc, output_sr)

    # Export to shapefile
    arcpy.AddMessage("Exporting shapefile...")
    arcpy.FeatureClassToShapefile_conversion([projected_fc], output_folder)

    # Rename all output files to match desired base name
    base_name = "projected_features"
    extensions = [".shp", ".shx", ".dbf", ".prj", ".cpg"]
    for ext in extensions:
        src = os.path.join(output_folder, base_name + ext)
        dst = os.path.join(output_folder, output_name + ext)
        if os.path.exists(src):
            os.rename(src, dst)

    arcpy.AddMessage(f"✅ Export complete: {os.path.join(output_folder, output_name)}.shp")

if __name__ == '__main__':
    main()
