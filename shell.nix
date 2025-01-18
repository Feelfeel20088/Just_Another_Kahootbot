{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312Packages.selenium
    pkgs.geckodriver
    pkgs.python312Packages.beautifulsoup4

  ];
}
