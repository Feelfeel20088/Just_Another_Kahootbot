{ lib, buildPythonPackage, pkgs }: 

buildPythonPackage rec { 
   pname = "kahoot-bot";
   version = "0.1.0";
   src = ./.;
   propagatedBuildInputs = [ 
     pkgs.python312Packages.selenium
     pkgs.geckodriver
     pkgs.python312Packages.beautifulsoup4
   ];
}
