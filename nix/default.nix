{
  pkgs,
  python313Packages,
}:

with pkgs; 

python313Packages.buildPythonApplication {
  name = "just_another_kahootbot";
  version = "v0.2.0-alpha";

  src = pkgs.fetchFromGitHub {
    owner = "Feelfeel20088";
    repo = "Just_Another_Kahootbot";
    rev = "v0.4.0-alpha"; 
    sha256 = " sha256-f9yyX8Zr1AwmmAEFZbne/v4NuVm6KfV7Y4qDky7x77A="; 
  };

  buildInputs = (with python313Packages; [
    pytest
  ]);

  propagatedBuildInputs = (with python313Packages; [
    httpx
    websockets
    quart
    pydantic
    orjson
    configargparse
  ]) ++ [ nodejs_24 ];

  # for docker
  postInstall = ''
    mkdir -p $out/app
    cp -r . $out/app/
  '';
  
  meta = {
    description = "Just_Another_Kahoot_Bot is a highly scalable, single-threaded bot for Kahoot, built for deployment on Kubernetes. Unlike traditional bots that rely on Selenium, this bot uses raw WebSockets, providing better performance, stability, and reliability. The bot can flood Kahoot games, answer questions correctly, and remain stealthy.";
    homepage = "https://github.com/Feelfeel20088/Just_Another_Kahootbot";
    license = lib.licenses.gpl3Only;
    maintainers = with lib.maintainers; [ Feelfeel20088 ];
  };
}