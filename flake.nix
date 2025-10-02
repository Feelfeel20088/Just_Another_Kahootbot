{
  description = "Dev shell Just_Another_Kahoot_Bot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs @ { self, nixpkgs, flake-utils, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = flake-utils.lib.defaultSystems;

      perSystem = { system, pkgs, ... }: let
        just_another_kahootbot = (pkgs.callPackage ./nix/default.nix {});
        
      in {
        packages = {
          default = just_another_kahootbot;

          dockerImage = pkgs.dockerTools.buildImage {
            name = "just_another_kahoot_bot";
            tag = "latest";

            # fromImage = pkgs.dockerTools.pullImage {
            #   imageName = "paketobuildpacks/nodejs";
            #   finalImageName = "paketobuildpacks/nodejs";
            #   finalImageTag = "latest";
            #   imageDigest = "sha256:8aaa7ef831b72dce5cfff67e5eaa651804fe43359a66c71c226651fc834ff53b";
            #   sha256 = "1VxV9ibVHHN9ABqDb0da9O2B6aiZipUlR3KUnhOkfnM=";
            # };

            config = {
              Cmd = ["just_another_kahootbot"];
              WorkingDir = "/app";
            };


            copyToRoot = pkgs.buildEnv {
              name = "just_another_kahootbot-docker-root";
              paths = [
                just_another_kahootbot
              ];
              pathsToLink = [ "/app" "/bin" ];
            };
          };
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.python313
            pkgs.python313Packages.httpx
            pkgs.python313Packages.websockets
            pkgs.python313Packages.quart
            pkgs.python313Packages.pydantic
            pkgs.python313Packages.orjson
            pkgs.python313Packages.pytest
            pkgs.python313Packages.configargparse
            pkgs.nodejs
            pkgs.yarn

            # linter
            # pkgs.python313Packages.ruff
          ];
        };
      };
    };
}
