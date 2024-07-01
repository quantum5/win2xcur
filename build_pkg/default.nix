{
  makesLib,
  nixpkgs,
  python_version,
  src,
}: let
  deps = import ./deps {
    inherit nixpkgs python_version;
  };

  # Define the package requirements
  build_required_deps = python_pkgs: {
    runtime_deps = with python_pkgs; [
      numpy
      wand
    ];
    build_deps = with python_pkgs; [flit-core];
    test_deps = with python_pkgs; [
      mypy
      pytest
      pylint
    ];
  };

  # The pkg builder
  bundle_builder = lib: pkgDeps:
    makesLib.makePythonPyprojectPackage {
      inherit (lib) buildEnv buildPythonPackage;
      inherit pkgDeps src;
    };

  # Abstract builder to allow an alternative to override dependencies
  build_bundle = builder:
  # builder: Deps -> (PythonPkgs -> PkgDeps) -> (Deps -> PkgDeps -> Bundle) -> Bundle
  # Deps: are the default project dependencies
  # PythonPkgs -> PkgDeps: is the required dependencies builder
  # Deps -> PkgDeps -> Bundle: is the bundle builder
    builder deps build_required_deps bundle_builder;

  # Concrete bundle that uses python pkgs from the default
  # i.e. the python nixpkg from the flake
  bundle = build_bundle (default: required_deps: builder: builder default.lib (required_deps default.python_pkgs));

  # Develompent environment
  dev_env = let
    template = makesLib.makePythonVscodeSettings {
      env = bundle.env.dev;
      bins = [ ];
      name = "win2xcur-env-dev-template";
    };
    hook = makesLib.makeScript {
      name = "win2xcur-env-dev";
      entrypoint = "${template}/template";
    };
  in nixpkgs.mkShell {
    packages = [bundle.env.dev];
    shellHook = "${hook}/bin/dev";
  };

  # Executable application derivation
  bin = deps.lib.toPythonApplication bundle.pkg;
in
  bundle // {inherit build_bundle dev_env bin;}
