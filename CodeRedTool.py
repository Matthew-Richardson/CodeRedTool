import arcpy
import os

def main():
    # Get inputs from ArcGIS Pro tool
    input_layer = arcpy.GetParameter(0)  # Feature Layer with selection
    output_folder = arcpy.GetParameterAsText(1)
    output_name = arcpy.GetParameterAsText(2)

    # NAD83 Geographic Coordinate System
    output_sr = arcpy.SpatialReference(4269)

    # Ensure features are selected
    desc = arcpy.Describe(input_layer)
    if not desc.FIDSet:
        arcpy.AddError("⚠️ No features selected in input layer.")
        raise ValueError("No selection.")

    # Set environment
    arcpy.env.workspace = "in_memory"
    arcpy.env.overwriteOutput = True

    arcpy.AddMessage("Copying selected features...")
    temp_fc = "in_memory/selected"
    arcpy.CopyFeatures_management(input_layer, temp_fc)

    arcpy.AddMessage("Reprojecting to NAD83 (EPSG:4269)...")
    projected_fc = "in_memory/projected"
    arcpy.Project_management(temp_fc, projected_fc, output_sr)

    arcpy.AddMessage("Exporting to shapefile...")
    arcpy.FeatureClassToShapefile_conversion([projected_fc], output_folder)

    # Rename files to match user-defined output name
    base_name = "projected"
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        src = os.path.join(output_folder, base_name + ext)
        dst = os.path.join(output_folder, output_name + ext)
        if os.path.exists(src):
            os.rename(src, dst)

    arcpy.AddMessage(f"✅ Export complete: {os.path.join(output_folder, output_name)}.shp")

if __name__ == '__main__':
    main()
