{
  nixpkgs,
  python_version,
}: let
  # Define required nixpkgs python builders
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    inherit (nixpkgs."${python_version}".pkgs) buildPythonPackage toPythonApplication;
    inherit (nixpkgs.python3Packages) fetchPypi;
  };
  # Define the nixpkgs python packages overrides
  python_pkgs = nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
}
