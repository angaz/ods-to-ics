{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

    devshell = {
      url = "github:numtide/devshell";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
    };
  };

  outputs = inputs@{
    self,
    nixpkgs,
    devshell,
    flake-parts,
    ...
  }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        devshell.flakeModule
        flake-parts.flakeModules.easyOverlay
      ];

      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem = { config, pkgs, system, ... }: {
        # Needs the scedule to be committed.
        # packages = {
        #   eth-berlin-ics =
        #     with pkgs.python311;
        #     buildPythonApplication {
        #       pname = "eth-berlin-ics";
        #       version = "0.0.1";

        #       propagatedBuildInputs = [
        #         pyexcel-ods
        #         ical
        #         aiohttp
        #       ];

        #       src = ./.;
        #     };
        # };

        devshells.default = {
          packages = with pkgs; [
            (python311.withPackages(p: with p; [
              pyexcel-ods
              ical
              aiohttp
            ]))
          ];
        };
      };
    };
}
