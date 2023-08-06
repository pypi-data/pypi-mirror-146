import labelbox

def make_dataset_and_data_rows(client: labelbox.Client, text_file_names: list[str], dataset_name: str) -> labelbox.Dataset:
    """
    Takes filenames  and creates a dataset with them
    Returns the dataset if you want to use it for anything else.
    """
    dataset = client.create_dataset(name=dataset_name)
    task = dataset.create_data_rows(text_file_names)
    status = task.wait_till_done()
    print("Labelbox dataset creation job complete.")
    return dataset