{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";
  };

  outputs =
    inputs:
    inputs.parts.lib.mkFlake { inherit inputs; } {
      systems = import inputs.systems;
      perSystem =
        { pkgs, ... }:
        {
          devShells.default = pkgs.mkShell {
            packages = with pkgs; [
              uv
              ruff
              basedpyright
            ];
          };
        };
    };
}
