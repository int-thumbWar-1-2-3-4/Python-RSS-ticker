import yaml


def yaml_loader(filepath):
    """
    View.gui_config.yaml_loader.

    Opens a yaml file and reads the data inside and returns it.
    """
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
    return data


def yaml_dump(filepath, info):
    """
        View.gui_config.yaml_dump.

        Opens a yaml file and writes the data given inside the yaml file.
        """
    with open(filepath, "w") as file:
        yaml.safe_dump(info, file)


if __name__ == "__main__":
    filepath = "gui_settings.yaml"
    data = yaml_loader(filepath)
    print(data)
