let
  metadata = (builtins.fromTOML (builtins.readFile ../pyproject.toml)).project;
in
  path_filter: src:
    path_filter {
      root = src;
      include = [
        "mypy.ini"
        "pyproject.toml"
        (path_filter.inDirectory metadata.name)
        (path_filter.inDirectory "tests")
      ];
    }
