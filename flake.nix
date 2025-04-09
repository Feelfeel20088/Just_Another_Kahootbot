{
  description = "dev shell and package for Just_Another_Kahoot_Bot"; # fill

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
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

        # Run a script after the dependencies are installed
        postShellHook = ''
          npm install
          ready! 
          cd ../
          python3 -m Just_Another_Kahoot_Bot 
        '';
      };
    };
}
