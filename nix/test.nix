{ pkgs, python313Packages }:

pkgs.stdenv.mkDerivation {
  name = "run-kahootbot-tests";

  buildInputs = [
    python313Packages.httpx
    python313Packages.websockets
    python313Packages.quart
    python313Packages.pydantic
    python313Packages.orjson
    python313Packages.configargparse
    python313Packages.pytest
    python313Packages.pytest-asyncio
  ];

  src = ../.;

  buildCommand = ''
    PYTHONPATH=$src pytest -v --asyncio-mode=auto
  '';
}
