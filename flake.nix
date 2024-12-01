{
  description = "dev env";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            (python3.withPackages (p: with p; [
              numpy
            ]))
            aoc-cli
          ];
          shellHook = ''
            export PATH="$(realpath ./bin):$PATH"
            export ADVENT_OF_CODE_SESSION=$(cat $(realpath ./.adventofcode.session))
          '';
        };
      });
}
