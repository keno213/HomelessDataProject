import pandas as pd
import boto3

def align_and_merge_datasets(anxiety_file, demographics_file, output_file, bucket_name):
    # Load datasets
    anxiety_data = pd.read_csv(anxiety_file)
    demographics_data = pd.read_csv(demographics_file)

    # Debugging: Print column names to verify
    print("Anxiety Data Columns:", anxiety_data.columns)
    print("Demographics Data Columns:", demographics_data.columns)

    # Normalize Homeless ID to match HID format
    anxiety_data["Homeless ID"] = anxiety_data["Homeless ID"].str.replace("HM15-", "", regex=False).str.strip()
    anxiety_data["Homeless ID"] = anxiety_data["Homeless ID"].str.zfill(3) + "-15"

    demographics_data["HID"] = demographics_data["HID"].str.strip()

    # Debugging: Print unique values in key columns
    print("Normalized Homeless IDs in Anxiety Data:", set(anxiety_data["Homeless ID"]))
    print("HIDs in Demographics Data:", set(demographics_data["HID"]))

    # Merge datasets on HID
    merged_data = pd.merge(
        anxiety_data,
        demographics_data,
        left_on="Homeless ID",
        right_on="HID",
        how="inner"
    )

    # Check if the merged DataFrame is empty
    if merged_data.empty:
        print("Warning: The merged dataset is empty. Please check the input files for mismatches.")
    else:
        # Save merged dataset
        merged_data.to_csv(output_file, index=False)
        print("Merged dataset saved.")

    # Upload to S3
    s3 = boto3.client('s3')
    try:
        s3.upload_file(output_file, bucket_name, output_file)
        print(f"{output_file} successfully uploaded to S3.")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Test function
if __name__ == "__main__":
    align_and_merge_datasets(
        "data/SF_HOMELESS_ANXIETY.csv",
        "data/SF_HOMELESS_DEMOGRAPHICS.csv",
        "merged_dataset.csv",
        "my-data-project-bucket"  # Bucket name passed as a string
    )
