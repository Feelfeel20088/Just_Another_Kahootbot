{
  description = "Dev shell Just_Another_Kahoot_Bot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.python313
            pkgs.python313Packages.requests
            pkgs.python313Packages.websockets
            pkgs.python313Packages.quart
            pkgs.python313Packages.pydantic
            pkgs.python313Packages.orjson
            pkgs.nodejs
            pkgs.yarn
          ];

          shellHook = ''
            echo "Installing Node dependencies..."
            npm install

            echo "Launching Just_Another_Kahoot_Bot..."
            cd ../
            python3 -m Just_Another_Kahoot_Bot
          '';
        };
      }
    );
}
