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
        extendedPkgs = pkgs.extend (import ./nix/default.nix {
          inherit pkgs;
        });
        
      in {
        packages = {
          default = extendedPkgs.just_another_kahoot_bot;

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
              Cmd = ["python" "-m" "Just_Another_Kahoot_Bot"];
              WorkingDir = "/app";
            };


            copyToRoot = pkgs.buildEnv {
              name = "felixhub-docker-root";
              paths = [
                pkgs.nodejs_22
                pkgs.python313
                pkgs.bash
                extendedPkgs.just_another_kahoot_bot
              ];
              pathsToLink = [ "/bin" "/app" ];
            };
          };
        };

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
        };
      };
    };
}
